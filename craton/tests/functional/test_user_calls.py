from craton.tests import functional


class UserTests(functional.TestCase):

    def test_create_user(self):
        project = self.create_project('test')
        url = self.url + '/v1/users'
        payload = {'username': 'testuser', 'project_id': project['id']}
        user = self.post(url, data=payload)
        self.assertEqual(201, user.status_code)
        self.assertEqual(payload['username'], user.json()['username'])
        self.assertEqual(payload['project_id'], user.json()['project_id'])

    def test_create_user_with_admin_priv(self):
        project = self.create_project('test')
        url = self.url + '/v1/users'
        payload = {'username': 'testuser', 'project_id': project['id'],
                   'is_admin': True}
        user = self.post(url, headers=self.root_headers, data=payload)
        self.assertEqual(201, user.status_code)
        self.assertEqual(payload['username'], user.json()['username'])
        self.assertEqual(payload['is_admin'], user.json()['is_admin'])

    def test_create_user_with_no_project_id_fails(self):
        url = self.url + '/v1/users'
        payload = {'username': 'testuser'}
        user = self.post(url, headers=self.root_headers, data=payload)
        self.assertEqual(400, user.status_code)
