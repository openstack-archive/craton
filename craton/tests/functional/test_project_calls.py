from craton.tests.functional import TestCase


class APIV1ProjectTest(TestCase):

    def setUp(self):
        super(APIV1ProjectTest, self).setUp(use_root=True)

    def tearDown(self):
        super(APIV1ProjectTest, self).tearDown()

    def create_project(self, name, variables=None):
        url = self.url + '/v1/projects'
        payload = {'name': name}
        if variables:
            payload['variables'] = variables
        project = self.post(url, data=payload)
        self.assertEqual(200, project.status_code)
        return project.json()

    def test_project_create_with_variables(self):
        variables = {"a": "b"}
        project_name = 'test'
        project = self.create_project(project_name, variables=variables)
        self.assertEqual(project_name, project['name'])
        self.assertEqual(variables, project['variables'])

    def test_cell_create_with_duplicate_name_works(self):
        project_name = 'test'
        self.create_project(project_name)
        url = self.url + '/v1/projects'
        payload = {'name': project_name}
        project = self.post(url, data=payload)
        self.assertEqual(200, project.status_code)

    def test_project_get_all_with_name_filter(self):
        proj1 = 'test1'
        proj2 = 'test2'
        self.create_project(proj2)
        for i in range(3):
            self.create_project(proj1)
        url = self.url + '/v1/projects?name=%s' % proj1
        resp = self.get(url)
        projects = resp.json()
        self.assertEqual(3, len(projects))
        for project in projects:
            self.assertEqual(proj1, project['name'])

    def test_get_project_details(self):
        project_name = 'test'
        project_vars = {"who": "that"}
        project = self.create_project(project_name, variables=project_vars)
        url = self.url + '/v1/projects/{}'.format(project['id'])
        project_with_detail = self.get(url)
        self.assertEqual(project_name, project_with_detail.json()['name'])
        self.assertEqual(project_vars, project_with_detail.json()['variables'])

    def test_project_delete(self):
        project1 = self.create_project('test1')
        url = self.url + '/v1/projects'
        projects = self.get(url)
        # NOTE(thomasem): Have to include the default project created by
        # test setup.
        self.assertEqual(2, len(projects.json()))

        delurl = self.url + '/v1/projects/{}'.format(project1['id'])
        self.delete(delurl)

        projects = self.get(url)
        self.assertEqual(1, len(projects.json()))

    def test_project_variables_update(self):
        project_name = 'test'
        project = self.create_project(project_name)
        variables = {"bumbleywump": "cucumberpatch"}

        put_url = self.url + '/v1/projects/{}/variables'.format(project['id'])
        resp = self.put(put_url, data=variables)
        self.assertEqual(200, resp.status_code)

        get_url = self.url + '/v1/projects/{}'.format(project['id'])
        project = self.get(get_url)
        self.assertEqual(variables, project.json()['variables'])
