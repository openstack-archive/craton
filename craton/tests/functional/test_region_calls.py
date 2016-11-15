from craton.tests.functional import TestCase


class APIV1RegionTest(TestCase):

    def setUp(self):
        super(APIV1RegionTest, self).setUp()

    def test_regions_get_all(self):
        url = self.url + '/v1/regions'
        resp = self.get(url)
        self.assertEqual(len(resp.json()), 2)

    def test_region_get_details_for_region_1(self):
        url = self.url + '/v1/regions/1'
        resp = self.get(url)
        region = resp.json()
        self.assertEqual('ORD135', region['name'])
