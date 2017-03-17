from oslo_utils import uuidutils

from craton.tests import functional


class UserTests(functional.TestCase):
    def setUp(self):
        super(UserTests, self).setUp()
        self.session.headers[functional.HEADER_USERNAME] = \
                functional.FAKE_DATA_GEN_BOOTSTRAP_USERNAME
        self.session.headers[functional.HEADER_TOKEN] = \
                functional.FAKE_DATA_GEN_BOOTSTRAP_TOKEN

    def tearDown(self):
        super(UserTests, self).tearDown()

    def create_project(self, name, variables=None):
        url = self.url + '/v1/projects'
        payload = {'name': name}
        if variables:
            payload['variables'] = variables
        response = self.post(url, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertIn('Location', response.headers)
        project = response.json()
        self.assertTrue(uuidutils.is_uuid_like(project['id']))
        self.assertEqual(
            response.headers['Location'],
            "{}/{}".format(url, project['id'])
        )

        return project

    def test_create_user(self):
        project = self.create_project('test')
        url = self.url + '/v1/users'
        payload = {'username': 'testuser', 'project_id': project['id']}
        user = self.post(url, data=payload)
        self.assertEqual(201, user.status_code)

    def test_create_user_with_no_project_id_fails(self):
        url = self.url + '/v1/users'
        payload = {'username': 'testuser'}
        user = self.post(url, data=payload)
        self.assertEqual(400, user.status_code)
