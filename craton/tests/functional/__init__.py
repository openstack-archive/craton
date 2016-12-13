import docker
import requests
from retrying import retry
import testtools
import threading


FAKE_DATA_GEN_USERNAME = 'demo'
FAKE_DATA_GEN_TOKEN = 'demo'
FAKE_DATA_GEN_PROJECT_ID = 'b9f10eca66ac4c279c139d01e65f96b4'


def get_client():
    client = docker.Client(version='auto')
    is_ok = client.ping()
    if is_ok != 'OK':
        msg = 'Docker daemon ping failed.'
        raise Exception(msg)
    return client


class DockerImageSetup(threading.Thread):

    def __init__(self):
        self.image_is_ready = threading.Event()
        self.error = None
        self.client = None
        self.repo_dir = './'
        super(DockerImageSetup, self).__init__()

    def run(self):
        """Build a docker container from the given Dockerfile and start
        the container in a separate thread."""
        try:
            self.client = get_client()
        except Exception as err:
            self.error = err
            self.image_is_ready.set()
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

        self.image_is_ready.set()


def start_container():
    # create and start the container
    client = get_client()
    container_tag = 'craton-functional-testing-api'
    container = client.create_container(container_tag)
    client.start(container)
    container_data = client.inspect_container(container)
    if container_data['State']['Status'] != 'running':
        msg = 'Container is not running.'
        raise Exception(msg)
    return container, container_data


def stop_container(container):
    """Stop a running container."""
    client = get_client()
    if container is not None:
        client.stop(container, timeout=30)


def remove_container(container):
    """Remove/Delete a stopped container."""
    client = get_client()
    if container is not None:
        client.remove_container(container)


def remove_image():
    """Remove the image we created."""
    client = get_client()
    client.remove_image('craton-functional-testing-api')


@retry(wait_fixed=1000, stop_max_attempt_number=20)
def ensure_running_endpoint(container_data):
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:8080/v1'.format(service_ip)
    headers = {"Content-Type": "application/json"}
    requests.get(url, headers=headers)


_image = None


def setup_image():
    global _image

    _image = DockerImageSetup()
    _image.daemon = True
    _image.start()
    _image.image_is_ready.wait()

    if _image.error:
        teardown_image()


def teardown_image():
    remove_image()


def setUpModule():
    setup_image()


def tearDownModule():
    teardown_image()


class TestCase(testtools.TestCase):

    def setUp(self):
        """Base setup provides container data back individual tests."""
        super(TestCase, self).setUp()
        self.image_build_error = _image.error
        self.error = None
        if not self.image_build_error:
            try:
                self.container, self.data = start_container()
                try:
                    ensure_running_endpoint(self.data)
                except Exception as err:
                    self.error = err
            except Exception as err:
                self.error = err

            self.service_ip = self.data['NetworkSettings']['IPAddress']
            self.url = 'http://{}:8080'.format(self.service_ip)
            self.headers = {'Content-Type': 'application/json'}
            self.headers['X-Auth-Project'] = FAKE_DATA_GEN_PROJECT_ID
            self.headers['X-Auth-Token'] = FAKE_DATA_GEN_TOKEN
            self.headers['X-Auth-User'] = FAKE_DATA_GEN_USERNAME

    def tearDown(self):
        super(TestCase, self).tearDown()
        stop_container(self.container)
        remove_container(self.container)

    def get(self, url):
        resp = requests.get(url, verify=False, headers=self.headers)
        return resp

    def post(self, url, **data):
        resp = requests.post(url, verify=False, headers=self.headers,
                             json=data)
        return resp

    def put(self, url, **data):
        resp = requests.put(url, verify=False, headers=self.headers,
                            json=data)
        return resp

    def delete(self, url):
        resp = requests.delete(url, verify=False, headers=self.headers)
        return resp
