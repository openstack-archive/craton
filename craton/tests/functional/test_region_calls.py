from craton.tests.functional import TestCase


class APIV1RegionTest(TestCase):
    """Test cases for /region calls.
    One set of data for the test is generated by fake data generateion
    script during test module setup.
    """

    def setUp(self):
        super(APIV1RegionTest, self).setUp()
        if self.image_build_error:
            raise Exception("Image Build failed: %s"
                    % self.image_build_error)
        if self.error:
            raise Exception("Container setup failed: %s"
                    % self.error)

    def make_region(self, **values):
        url = self.url + '/v1/regions'
        resp = self.post(url, **values)
        return resp

    def test_create_region_full_data(self):
        # Test with full set of allowed parameters
        values = {"name": "region-new",
                  "note": "This is region-new.",
                  "variables": {"a": "b"}}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(values["name"], resp.json()['name'])
        self.assertEqual(values["variables"], resp.json()['variables'])

    def test_create_region_without_variables(self):
        values = {"name": "region-two",
                  "note": "This is region-two"}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(values["name"], resp.json()['name'])
        self.assertEqual({}, resp.json()['variables'])

    def test_create_region_with_no_name_fails(self):
        values = {"note": "This is region one."}
        resp = self.make_region(**values)
        self.assertEqual(resp.status_code, 422)
        err_msg = ["'name' is a required property"]
        self.assertEqual(resp.json()['errors'], err_msg)

    def test_create_region_with_duplicate_name_fails(self):
        values = {"name": "region-1"}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)
        # Now make the same region again
        resp = self.make_region(**values)
        self.assertEqual(409, resp.status_code)

    def test_region_delete(self):
        values = {"name": "region-1"}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)
        region_id = resp.json()['id']
        url = self.url + '/v1/regions/{}'.format(region_id)
        resp = self.delete(url)
        self.assertEqual(resp.status_code, 204)

    def test_regions_get_all(self):
        reg1 = {"name": "region-1"}
        reg2 = {"name": "region-2"}
        resp = self.make_region(**reg1)
        self.assertEqual(200, resp.status_code)
        resp = self.make_region(**reg2)
        self.assertEqual(200, resp.status_code)

        url = self.url + '/v1/regions'
        resp = self.get(url)
        self.assertEqual(2, len(resp.json()))

    def test_regions_get_all_with_name_filter(self):
        values = {"name": "ORD135"}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)

        url = self.url + '/v1/regions?name=ORD135'
        resp = self.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual('ORD135', resp.json()[0]['name'])

    def test_region_with_non_existing_filters(self):
        url = self.url + '/v1/regions?name=idontexist'
        resp = self.get(url)
        self.assertEqual(404, resp.status_code)

    def test_region_get_details_for_region(self):
        values = {"name": "region-1",
                  "variables": {"a": "b"}}
        resp = self.make_region(**values)
        self.assertEqual(200, resp.status_code)
        region_id = resp.json()['id']
        url = self.url + '/v1/regions/{}'.format(region_id)
        self.get(url)
        self.assertEqual('region-1', resp.json()['name'])
        self.assertEqual(values['variables'], resp.json()['variables'])
