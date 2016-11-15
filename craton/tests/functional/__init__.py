import docker
import requests
from retrying import retry
import testtools
import threading
import subprocess


FAKE_DATA_GEN_USERNAME = 'demo'
FAKE_DATA_GEN_TOKEN = 'demo'
FAKE_DATA_GEN_PROJECT_ID = 'b9f10eca66ac4c279c139d01e65f96b4'


class DockerSetup(threading.Thread):

    def __init__(self):
        self.container = None
        self.container_is_ready = threading.Event()
        self.error = None
        self.client = None
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
        build_output = self.client.build(path='github.com/openstack/craton',
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
        """Remove/Delete a stopeed container."""
        if self.container is not None:
            self.client.remove_container(self.container)

    def remove_image(self):
        """Remove the image we created."""
        if self.client:
            self.client.remove_image('craton-functional-testing-api')


def generate_fake_data(container_data):
    """Run data generation script."""
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:8080/v1'.format(service_ip)

    subprocess.run(["python", "./tools/generate_fake_data.py", "--url",
                   url, "--user", FAKE_DATA_GEN_USERNAME, "--key",
                   FAKE_DATA_GEN_TOKEN, "--project",
                   FAKE_DATA_GEN_PROJECT_ID], check=True)


@retry(wait_fixed=1000, stop_max_attempt_number=20)
def ensure_running_endpoint(container_data):
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:8080/v1'.format(service_ip)
    headers = {"Content-Type": "application/json"}
    requests.get(url, headers=headers)


_container = None
container_setup_error = None
container_data = None


def setup_container():
    global _container
    global container_setup_error
    global container_data

    _container = DockerSetup()
    _container.daemon = True
    _container.start()
    _container.container_is_ready.wait()
    container_setup_error = _container.error

    if container_setup_error:
        teardown_container()
    else:
        try:
            container_data = _container.container_data
            ensure_running_endpoint(container_data)
            generate_fake_data(container_data)
        except Exception:
            msg = 'Error during data generation script run.'
            container_setup_error = msg
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


class TestCase(testtools.TestCase):

    def setUp(self):
        """Base setup provides container data back individual tests."""
        super(TestCase, self).setUp()
        self.container_setup_error = container_setup_error
        # In case of container_setup_error tests get skipped
        if not self.container_setup_error:
            self.service_ip = container_data['NetworkSettings']['IPAddress']
            self.url = 'http://{}:8080/'.format(self.service_ip)
            self.headers = {'Content-Type': 'application/json'}
            self.headers['X-Auth-Project'] = FAKE_DATA_GEN_PROJECT_ID
            self.headers['X-Auth-Token'] = FAKE_DATA_GEN_TOKEN
            self.headers['X-Auth-User'] = FAKE_DATA_GEN_USERNAME

    def get(self, url, **data):
        resp = requests.get(url, verify=False, headers=self.headers,
                            json=data)
        return resp

    def post(self, url, **data):
        return None

    def put(self, url, **data):
        return None

    def delete(self, url, **data):
        return None
