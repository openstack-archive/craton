from craton.tests.functional import TestCase


class APIV1ResourceWithVariablesTestCase(TestCase):
    """Base test case for resources that have variables mixed in"""

    resource = '<resource>'  # Test classes that mix in should set
    path = '/v1/{resource}/{resource_id}/variables'

    def get_vars_url(self, resource_id):
        return self.url + self.path.format(
            resource=self.resource, resource_id=resource_id)

    def get_current_vars(self, resource_id):
        url = self.get_vars_url(resource_id)
        response = self.get(url)
        self.assertEqual(200, response.status_code)
        return response.json()['variables']

    def assert_vars_get_expected(self, resource_id, expected_vars):
        self.assertEqual(expected_vars, self.get_current_vars(resource_id))

    def assert_vars_can_be_set(self, resource_id):
        """Asserts new vars can be added to the existing vars, if any"""
        # track the expected current state of vars for this resource,
        # verifying expectations
        current_vars = self.get_current_vars(resource_id)
        payload = {'string-key': 'string-value', 'num-key': 47,
                   'bookean-key': False, 'none-key': None,
                   'object-key': {'a': 1, 'b': 2},
                   'list-key': ['a', 'b', 1, 2, 3, True, None]}

        url = self.get_vars_url(resource_id)
        response = self.put(url, data=payload)
        current_vars.update(payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual(current_vars, response.json()['variables'])
        self.assertEqual(current_vars, self.get_current_vars(resource_id))

    def assert_vars_can_be_deleted(self, resource_id):
        """Asserts that new vars can be added, then deleted"""
        # track the expected current state of vars for this resource,
        # verifying expectations
        current_vars = self.get_current_vars(resource_id)

        url = self.get_vars_url(resource_id)
        added_vars = {'will-keep': 42, 'will-delete': 47}
        response = self.put(url, data=added_vars)
        current_vars.update(added_vars)
        self.assertEqual(200, response.status_code)
        self.assertEqual(current_vars, response.json()['variables'])
        self.assertEqual(current_vars, self.get_current_vars(resource_id))

        response = self.delete(url, body=['will-delete', 'non-existent-key'])
        del current_vars['will-delete']
        self.assertEqual(204, response.status_code)
        self.assertEqual(current_vars, self.get_current_vars(resource_id))
