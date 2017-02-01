import contextlib
import docker
import requests
from retrying import retry
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import testtools
import threading


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
                self.container_is_ready.set()
                return
        except Exception as err:
            self.error = err
            self.container_is_ready.set()
            return

        # Create Docker image for Craton
        build_output = self.client.build(path=self.repo_dir,
                                         tag='craton-functional-testing-api',
                                         dockerfile='Dockerfile',
                                         pull=True,
                                         forcerm=True)
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
    url = 'http://{}:8080/v1'.format(service_ip)
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

    with contextlib.closing(engine.connect()) as conn:
        transaction = conn.begin()
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        transaction.commit()

    # NOTE(sulo): as a part of db setup, we bootstrap user and project
    # Although, project and user might have been bootstrapped externally
    # we clean the db up for tests, and do our own bootstrapping to
    # isolate all test from any external scripts.
    projects = meta.tables['projects']
    users = meta.tables['users']

    with contextlib.closing(engine.connect()) as conn:
        transaction = conn.begin()
        conn.execute(projects.insert(),
                     name=FAKE_DATA_GEN_USERNAME,
                     id=FAKE_DATA_GEN_PROJECT_ID)
        conn.execute(users.insert(),
                     project_id=FAKE_DATA_GEN_PROJECT_ID,
                     username=FAKE_DATA_GEN_USERNAME,
                     api_key=FAKE_DATA_GEN_TOKEN,
                     is_admin=True)
        conn.execute(users.insert(),
                     project_id=FAKE_DATA_GEN_PROJECT_ID,
                     username=FAKE_DATA_GEN_BOOTSTRAP_USERNAME,
                     api_key=FAKE_DATA_GEN_BOOTSTRAP_TOKEN,
                     is_admin=True,
                     is_root=True)
        transaction.commit()


class TestCase(testtools.TestCase):

    def setUp(self):
        """Base setup provides container data back individual tests."""
        super(TestCase, self).setUp()
        self.container_setup_error = _container.error
        self.session = requests.Session()
        if not self.container_setup_error:
            data = _container.container_data
            self.service_ip = data['NetworkSettings']['IPAddress']
            self.url = 'http://{}:8080'.format(self.service_ip)
            self.session.headers[HEADER_PROJECT] = FAKE_DATA_GEN_PROJECT_ID
            self.session.headers[HEADER_USERNAME] = FAKE_DATA_GEN_USERNAME
            self.session.headers[HEADER_TOKEN] = FAKE_DATA_GEN_TOKEN

        setup_database(self.service_ip)

    def tearDown(self):
        super(TestCase, self).tearDown()

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
