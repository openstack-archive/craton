from craton.tests import functional
from craton.tests.functional.test_variable_calls import \
    APIV1ResourceWithVariablesTestCase


class TestPaginationOfProjects(functional.TestCase):
    def setUp(self):
        super(TestPaginationOfProjects, self).setUp()
        self.projects = [
            self.create_project('project-{}'.format(i))
            for i in range(0, 61)
        ]

    def test_lists_first_thirty_projects(self):
        response = self.get(self.url + '/v1/projects',
                            headers=self.root_headers)
        self.assertSuccessOk(response)
        json = response.json()
        self.assertIn('projects', json)
        projects = json['projects']
        self.assertEqual(30, len(projects))

    def test_lists_projects_with_the_same_name(self):
        self.create_project('project-0')

        response = self.get(self.url + '/v1/projects',
                            name='project-0',
                            headers=self.root_headers)
        self.assertSuccessOk(response)
        projects = response.json()['projects']
        self.assertEqual(2, len(projects))


class APIV1ProjectTest(APIV1ResourceWithVariablesTestCase):

    resource = 'projects'

    def test_project_create_with_variables(self):
        variables = {'a': 'b'}
        project_name = 'test'
        project = self.create_project(project_name, variables=variables)
        self.assertEqual(project_name, project['name'])
        self.assertEqual(variables, project['variables'])

    def test_create_project_supports_vars_ops(self):
        project = self.create_project('test', variables={'a': 'b'})
        self.assert_vars_get_expected(project['id'], {'a': 'b'})
        self.assert_vars_can_be_set(project['id'])
        self.assert_vars_can_be_deleted(project['id'])

    def test_project_create_with_duplicate_name_works(self):
        project_name = 'test'
        self.create_project(project_name)
        url = self.url + '/v1/projects'
        payload = {'name': project_name}
        project = self.post(url, headers=self.root_headers, data=payload)
        self.assertEqual(201, project.status_code)

    def test_project_get_all_with_name_filter(self):
        proj1 = 'test1'
        proj2 = 'test2'
        self.create_project(proj2)
        for i in range(3):
            self.create_project(proj1)
        url = self.url + '/v1/projects?name={}'.format(proj1)
        resp = self.get(url, headers=self.root_headers)
        projects = resp.json()['projects']
        self.assertEqual(3, len(projects))
        for project in projects:
            self.assertEqual(proj1, project['name'])

    def test_get_project_details(self):
        project_name = 'test'
        project_vars = {"who": "that"}
        project = self.create_project(project_name, variables=project_vars)
        url = self.url + '/v1/projects/{}'.format(project['id'])
        project_with_detail = self.get(url, headers=self.root_headers)
        self.assertEqual(project_name, project_with_detail.json()['name'])
        self.assertEqual(project_vars, project_with_detail.json()['variables'])

    def test_project_delete(self):
        project1 = self.create_project('test1')
        url = self.url + '/v1/projects'
        projects = self.get(url, headers=self.root_headers)
        # NOTE(thomasem): Have to include the default project created by
        # test setup.
        self.assertEqual(2, len(projects.json()['projects']))

        delurl = self.url + '/v1/projects/{}'.format(project1['id'])
        self.delete(delurl, headers=self.root_headers)

        projects = self.get(url, headers=self.root_headers)
        self.assertEqual(1, len(projects.json()['projects']))

    def test_project_variables_update(self):
        project_name = 'test'
        project = self.create_project(project_name)
        variables = {"bumbleywump": "cucumberpatch"}

        put_url = self.url + '/v1/projects/{}/variables'.format(project['id'])
        resp = self.put(put_url, headers=self.root_headers, data=variables)
        self.assertEqual(200, resp.status_code)

        get_url = self.url + '/v1/projects/{}'.format(project['id'])
        project = self.get(get_url, headers=self.root_headers)
        self.assertEqual(variables, project.json()['variables'])

    def test_project_variables_delete(self):
        project_name = 'test'
        delete_key = 'bumbleywump'
        variables = {
            delete_key: 'cucumberpatch'
        }
        expected_vars = {'foo': 'bar'}
        variables.update(expected_vars)

        project = self.create_project(project_name, variables=variables)
        self.assert_vars_get_expected(project['id'], variables)
        self.assert_vars_can_be_deleted(project['id'])
