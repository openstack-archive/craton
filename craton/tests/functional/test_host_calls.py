from craton.tests.functional import TestCase


class APIV1HostTest(TestCase):

    def setUp(self):
        super(APIV1HostTest, self).setUp()

    def test_host_get_all_for_region_1(self):
        url = self.url + '/v1/hosts?region_id=1'
        resp = self.get(url)
        self.assertEqual(len(resp.json()), 8)
