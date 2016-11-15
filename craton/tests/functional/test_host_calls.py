from craton.tests.functional import TestCase

import json
import requests


class APIV1HostTest(TestCase):

    def setUp(self):
        super(APIV1HostTest, self).setUp()
        if self.container_setup_error:
            self.skipTest('Error setting up service container')

    def test_host_get_all_for_region_1(self):
        url = self.url + '/v1/hosts?region_id=1'
        resp = self.get(url)
        self.assertEqual(len(resp.json()), 8)
