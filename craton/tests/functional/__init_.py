import threading
import testtools
import subprocess
from time import sleep
import requests
import docker


class DockerSetup(threading.Thread):

    def __init__(self):
        self.container = None
        self.container_is_ready = threading.Event()
        self.error = None
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
        except ConnectionError as err:
            self.error = err
            raise

        # Create Docker image for Craton
        build_output = self.client.build(path='github.com/openstack/craton',
                                         tag='craton-api',
                                         dockerfile='Dockerfile',
                                         forcerm=True)
        output_last_line = None
        for line in build_output:
            output_last_line = line

        message = output_last_line.decode("utf-8")
        if "Successfully built" not in message:
            msg = 'Failed to build docker image.'
            self.error = msg
            raise Exception(msg)

        # create and start the container
        self.container = self.client.create_container('craton-api')
        self.client.start(self.container)
        self.container_data = self.client.inspect_container(self.container)
        if self.container_data['State']['Status'] != 'running':
            msg = 'Container is not running.'
            self.error = msg
            raise Exception(msg)

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
        self.client.remove_image('craton-api')


def generate_fake_data(container_data):
    """Run data generation script."""
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:8080/v1'.format(service_ip)
    user = key = 'demo'
    project = 'b9f10eca66ac4c279c139d01e65f96b4'

    subprocess.run(["python", "./tools/generate_fake_data.py", "--url",
                   url, "--user", user, "--key", key, "--project",
                   project], check=True)


def ensure_running_endpoint(container_data, retry=30):
    service_ip = container_data['NetworkSettings']['IPAddress']
    url = 'http://{}:8080/v1'.format(service_ip)
    retries = 0
    while retries < retry:
        try:
            headers = {"Content-Type": "application/json"}
            requests.get(url, headers=headers)
            break
        except requests.ConnectionError:
            retries += 1
            sleep(1)

    if retries == 30:
        raise Exception("No of retries reached for starting endpoint")


class TestCase(testtools.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once per class of tests. Setups the container and
        generates fake data for the test."""
        cls.container = DockerSetup()
        cls.container.daemon = True
        cls.container.start()
        cls.container.container_is_ready.wait()
        cls.container_setup_error = cls.container.error
        cls.container_data = cls.container.container_data

        if cls.container_setup_error:
            cls.tearDownClass()

        try:
            ensure_running_endpoint(cls.container_data)
            generate_fake_data(cls.container_data)
        except subprocess.CalledProcessError:
            msg = 'Error during data generation script run.'
            cls.container_setup_error = msg
            cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        cls.container.stop()
        cls.container.remove()
        cls.container.remove_image()
