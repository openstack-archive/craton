import contextlib
import threading

import docker
from oslo_log import log as logging
import requests
from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
import testtools

from craton.db.sqlalchemy import models


LOG = logging.getLogger(__name__)


FAKE_DATA_GEN_USERNAME = 'demo'
FAKE_DATA_GEN_TOKEN = 'demo'
FAKE_DATA_GEN_PROJECT_ID = 'b9f10eca66ac4c279c139d01e65f96b4'

FAKE_DATA_GEN_BOOTSTRAP_USERNAME = 'bootstrap'
FAKE_DATA_GEN_BOOTSTRAP_TOKEN = 'bootstrap'

HEADER_TOKEN = 'X-Auth-Token'
HEADER_USERNAME = 'X-Auth-User'
HEADER_PROJECT = 'X-Auth-Project'


class DockerSetup(threading.Thread):

    def __init__(self):
        self.container = None
        self.container_is_ready = threading.Event()
        self.error = None
        self.client = None
        self.repo_dir = './'
        super(DockerSetup, self).__init__()

    def run(self):
        """Build a docker container from the given Dockerfile and start
        the container in a separate thread."""
        try:
            self.client = docker.Client(version='auto')
            is_ok = self.client.ping()
            if is_ok != 'OK':
                msg = 'Docker daemon ping failed.'
                self.error = msg
                LOG.error(self.error)
                self.container_is_ready.set()
                return
        except Exception as err:
            self.error = err
            LOG.error(self.error)
            self.container_is_ready.set()
            return

        # Create Docker image for Craton
        build_output = self.client.build(path=self.repo_dir,
                                         tag='craton-functional-testing-api',
                                         dockerfile='Dockerfile',
                                         pull=True,
                                         forcerm=True)
        LOG.debug(build_output)
        output_last_line = ""
        for output_last_line in build_output:
            pass

        message = output_last_line.decode("utf-8")
        if "Successfully built" not in message:
            msg = 'Failed to build docker image.'
            self.error = msg
            self.container_is_ready.set()
            return

        # create and start the container
        container_tag = 'craton-functional-testing-api'
        self.container = self.client.create_container(container_tag)
        self.client.start(self.container)
        self.container_data = self.client.inspect_container(self.container)
        if self.container_data['State']['Status'] != 'running':
            msg = 'Container is not running.'
            self.error = msg
            self.container_is_ready.set()
            return

        self.container_is_ready.set()

    def stop(self):
        """Stop a running container."""
        if self.container is not None:
            self.client.stop(self.container, timeout=30)

    def remove(self):
        """Remove/Delete a stopped container."""
        if self.container is not None:
            self.client.remove_container(self.container)

    def remove_image(self):
        """Remove the image we created."""
        if self.client:
            self.client.remove_image('craton-functional-testing-api')


@retry(wait_fixed=1000, stop_max_attempt_number=20)
def ensure_running_endpoint(container_data):
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:7780/v1'.format(service_ip)
    headers = {"Content-Type": "application/json"}
    requests.get(url, headers=headers)


_container = None


def setup_container():
    global _container

    _container = DockerSetup()
    _container.daemon = True
    _container.start()
    _container.container_is_ready.wait()

    if _container.error:
        teardown_container()
    else:
        try:
            ensure_running_endpoint(_container.container_data)
        except Exception:
            msg = 'Error during data generation script run.'
            _container.error = msg
            teardown_container()


def teardown_container():
    if _container:
        _container.stop()
        _container.remove()
        _container.remove_image()


def setUpModule():
    setup_container()


def tearDownModule():
    teardown_container()


def setup_database(container_ip):
    mysqldb = "mysql+pymysql://craton:craton@{}/craton".format(container_ip)
    engine = create_engine(mysqldb)
    meta = MetaData()
    meta.reflect(engine)

    # NOTE(sulo, jimbaker): First clean the db up for tests, and do
    # our own bootstrapping to isolate all test from any external
    # scripts.
    with contextlib.closing(engine.connect()) as conn:
        transaction = conn.begin()
        conn.execute("SET foreign_key_checks = 0")
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        conn.execute("SET foreign_key_checks = 1")
        transaction.commit()

    # NOTE(sulo, jimbaker): now bootstrap user and project; using the
    # SA model allows us to respect the additional constraints in the
    # model, vs having to duplicate logic if working against the
    # database directly.
    Session = sessionmaker(bind=engine)
    session = Session()
    project = models.Project(
        name=FAKE_DATA_GEN_USERNAME,
        id=FAKE_DATA_GEN_PROJECT_ID)
    bootstrap_user = models.User(
        project=project,
        username=FAKE_DATA_GEN_BOOTSTRAP_USERNAME,
        api_key=FAKE_DATA_GEN_BOOTSTRAP_TOKEN,
        is_admin=True,
        is_root=True)
    demo_user = models.User(
        project=project,
        username=FAKE_DATA_GEN_USERNAME,
        api_key=FAKE_DATA_GEN_TOKEN,
        is_admin=True)

    session.add(project)
    session.add(bootstrap_user)
    session.add(demo_user)

    # NOTE(jimbaker) simple assumption: either this commit succeeds,
    # or we need to fail fast - there's no recovery allowed in this
    # testing setup.
    session.commit()


class TestCase(testtools.TestCase):

    def setUp(self):
        """Base setup provides container data back individual tests."""
        super(TestCase, self).setUp()
        self.container_setup_error = _container.error
        self.session = requests.Session()
        if not self.container_setup_error:
            data = _container.container_data
            self.service_ip = data['NetworkSettings']['IPAddress']
            self.url = 'http://{}:7780'.format(self.service_ip)
            self.session.headers[HEADER_PROJECT] = FAKE_DATA_GEN_PROJECT_ID
            self.session.headers[HEADER_USERNAME] = FAKE_DATA_GEN_USERNAME
            self.session.headers[HEADER_TOKEN] = FAKE_DATA_GEN_TOKEN

        setup_database(self.service_ip)

    def tearDown(self):
        super(TestCase, self).tearDown()

    def assertSuccessOk(self, response):
        self.assertEqual(requests.codes.OK, response.status_code)

    def assertSuccessCreated(self, response):
        self.assertEqual(requests.codes.CREATED, response.status_code)

    def assertNoContent(self, response):
        self.assertEqual(requests.codes.NO_CONTENT, response.status_code)

    def assertBadRequest(self, response):
        self.assertEqual(requests.codes.BAD_REQUEST, response.status_code)

    def get(self, url, headers=None, **params):
        resp = self.session.get(
            url, verify=False, headers=headers, params=params,
        )
        return resp

    def post(self, url, headers=None, data=None):
        resp = self.session.post(
            url, verify=False, headers=headers, json=data,
        )
        return resp

    def put(self, url, headers=None, data=None):
        resp = self.session.put(
            url, verify=False, headers=headers, json=data,
        )
        return resp

    def delete(self, url, headers=None, body=None):
        resp = self.session.delete(
            url, verify=False, headers=headers, json=body,
        )
        return resp

    def create_cloud(self, name, variables=None):
        url = self.url + '/v1/clouds'

        values = {'name': name}
        if variables:
            values['variables'] = variables
        resp = self.post(url, data=values)
        self.assertSuccessCreated(resp)
        self.assertIn('Location', resp.headers)
        json = resp.json()
        self.assertEqual(
            resp.headers['Location'],
            "{}/{}".format(url, json['id'])
        )
        return json

    def delete_clouds(self, clouds):
        base_url = self.url + '/v1/clouds/{}'
        for cloud in clouds:
            url = base_url.format(cloud['id'])
            resp = self.delete(url)
            self.assertNoContent(resp)

    def create_region(self, name, cloud, variables=None):
        url = self.url + '/v1/regions'

        values = {'name': name, 'cloud_id': cloud['id']}
        if variables:
            values['variables'] = variables
        resp = self.post(url, data=values)
        self.assertSuccessCreated(resp)
        self.assertIn('Location', resp.headers)
        json = resp.json()
        self.assertEqual(
            resp.headers['Location'],
            "{}/{}".format(url, json['id'])
        )
        return json

    def delete_regions(self, regions):
        base_url = self.url + '/v1/regions/{}'
        for region in regions:
            url = base_url.format(region['id'])
            resp = self.delete(url)
            self.assertNoContent(resp)

    def create_cell(self, name, cloud, region, variables=None):
        url = self.url + '/v1/cells'
        payload = {'name': name, 'region_id': region['id'],
                   'cloud_id': cloud['id']}
        if variables:
            payload['variables'] = variables
        cell = self.post(url, data=payload)
        self.assertEqual(201, cell.status_code)
        self.assertIn('Location', cell.headers)
        self.assertEqual(
            cell.headers['Location'],
            "{}/{}".format(url, cell.json()['id'])
        )
        return cell.json()

    def create_host(self, name, cloud, region, hosttype, ip_address,
                    parent_id=None, **variables):
        url = self.url + '/v1/hosts'
        payload = {
            'name': name,
            'device_type': hosttype,
            'ip_address': ip_address,
            'region_id': region['id'],
            'cloud_id': cloud['id']
        }
        if parent_id:
            payload['parent_id'] = parent_id
        if variables:
            payload['variables'] = variables

        host = self.post(url, data=payload)
        self.assertEqual(201, host.status_code)
        self.assertIn('Location', host.headers)
        self.assertEqual(
            host.headers['Location'],
            "{}/{}".format(url, host.json()['id'])
        )
        return host.json()

    def create_network_device(
            self, name, cloud, region, device_type, ip_address, parent_id=None,
            **variables
            ):

        url = self.url + '/v1/network-devices'
        payload = {
            'name': name,
            'device_type': device_type,
            'ip_address': ip_address,
            'region_id': region['id'],
            'cloud_id': cloud['id'],
        }
        if parent_id:
            payload['parent_id'] = parent_id
        if variables:
            payload['variables'] = variables

        network_device = self.post(url, data=payload)
        self.assertEqual(201, network_device.status_code)
        self.assertIn('Location', network_device.headers)
        self.assertEqual(
            network_device.headers['Location'],
            "{}/{}".format(url, network_device.json()['id'])
        )
        return network_device.json()


class DeviceTestBase(TestCase):
    def setUp(self):
        super(DeviceTestBase, self).setUp()
        self.cloud = self.create_cloud()
        self.region = self.create_region()

    def create_cloud(self, name='cloud-1'):
        return super(DeviceTestBase, self).create_cloud(name=name)

    def create_region(self, name='region-1', cloud=None, variables=None):
        return super(DeviceTestBase, self).create_region(
            name=name,
            cloud=cloud if cloud else self.cloud,
            variables=variables,
        )

    def create_network_device(self, name, device_type, ip_address, region=None,
                              cloud=None, parent_id=None, **variables):
        return super(DeviceTestBase, self).create_network_device(
            name=name,
            cloud=cloud if cloud else self.cloud,
            region=region if region else self.region,
            device_type=device_type,
            ip_address=ip_address,
            parent_id=parent_id,
            **variables
        )

    def create_host(self, name, hosttype, ip_address, region=None, cloud=None,
                    parent_id=None, **variables):
        return super(DeviceTestBase, self).create_host(
            name=name,
            cloud=cloud if cloud else self.cloud,
            region=region if region else self.region,
            hosttype=hosttype,
            ip_address=ip_address,
            parent_id=parent_id,
            **variables
        )
