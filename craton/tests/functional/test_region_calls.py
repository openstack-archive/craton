from craton.tests.functional import TestCase


class APIV1RegionTest(TestCase):
    """Test cases for /region calls.
    One set of data for the test is generated by fake data generateion
    script during test module setup.
    """

    def setUp(self):
        super(APIV1RegionTest, self).setUp()

    def create_region(self, name, variables=None):
        url = self.url + '/v1/regions'

        values = {'name': name}
        if variables:
            values['variables'] = variables
        resp = self.post(url, data=values)
        self.assertEqual(200, resp.status_code)
        return resp.json()

    def test_create_region_full_data(self):
        # Test with full set of allowed parameters
        values = {"name": "region-new",
                  "note": "This is region-new.",
                  "variables": {"a": "b"}}
        url = self.url + '/v1/regions'
        resp = self.post(url, data=values)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(values['name'], resp.json()['name'])

    def test_create_region_without_variables(self):
        values = {"name": "region-two",
                  "note": "This is region-two"}
        url = self.url + '/v1/regions'
        resp = self.post(url, data=values)
        self.assertEqual(200, resp.status_code)
        self.assertEqual("region-two", resp.json()['name'])

    def test_create_region_with_no_name_fails(self):
        values = {"note": "This is region one."}
        url = self.url + '/v1/regions'
        resp = self.post(url, data=values)
        self.assertEqual(resp.status_code, 422)
        err_msg = ["'name' is a required property"]
        self.assertEqual(resp.json()['errors'], err_msg)

    def test_create_region_with_duplicate_name_fails(self):
        self.create_region("ORD135")

        values = {"name": "ORD135"}
        url = self.url + '/v1/regions'
        resp = self.post(url, data=values)
        self.assertEqual(409, resp.status_code)

    def test_regions_get_all(self):
        self.create_region("ORD1")
        self.create_region("ORD2")
        url = self.url + '/v1/regions'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.json()))

    def test_regions_get_all_with_name_filter(self):
        self.create_region("ORD1")
        self.create_region("ORD2")
        url = self.url + '/v1/regions?name=ORD1'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(resp.json()))
        self.assertEqual('ORD1', resp.json()[0]['name'])

    def test_region_with_non_existing_filters(self):
        self.create_region("ORD1")
        url = self.url + '/v1/regions?name=idontexist'
        resp = self.get(url)
        self.assertEqual(404, resp.status_code)

    def test_region_get_details_for_region(self):
        regvars= {"a":"b", "one": "two"}
        region = self.create_region("ORD1", variables=regvars)
        url = self.url + '/v1/regions/{}'.format(region['id'])
        resp = self.get(url)
        region = resp.json()
        self.assertEqual(region['name'], 'ORD1')
        self.assertEqual(regvars, region['variables'])
