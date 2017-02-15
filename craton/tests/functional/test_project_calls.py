from craton.tests import functional


class TestPaginationOfProjects(functional.TestCase):
    def setUp(self):
        super(TestPaginationOfProjects, self).setUp()
        self.url = self.url + '/v1/projects'
        self.projects = [
            self.create_project('project-{}'.format(i))
            for i in range(0, 61)
        ]

    def create_project(self, project_name='project-0'):
        payload = {'name': project_name}
        response = self.post(self.url, data=payload)
        self.assertSuccessCreated(response)
        return response.json()

    def test_lists_first_thirty_projects(self):
        response = self.get(self.url)
        self.assertSuccessOk(response)
        json = response.json()
        self.assertIn('projects', json)
        projects = json['projects']
        self.assertEqual(30, len(projects))
        self.assertListEqual([p['id'] for p in self.projects[:30]],
                             [p['id'] for p in projects])

    def test_list_with_name_filter(self):
        url = self.url + '?name=' + self.projects[0]['name']
        response = self.get(url)
        self.assertSuccessOk(response)
        projects = response.json()['projects']
        self.assertEqual(1, len(projects))
