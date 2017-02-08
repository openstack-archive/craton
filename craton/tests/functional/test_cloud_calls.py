import urllib.parse

from craton.tests.functional import TestCase


class APIV1CloudTest(TestCase):
    """Test cases for /cloud calls.
    """

    def test_create_cloud_full_data(self):
        # Test with full set of allowed parameters
        values = {"name": "cloud-new",
                  "note": "This is cloud-new.",
                  "variables": {"a": "b"}}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)
        self.assertEqual(
            resp.headers['Location'],
            "{}/{}".format(url, resp.json()['id'])
        )
        self.assertEqual(values['name'], resp.json()['name'])

    def test_create_cloud_without_variables(self):
        values = {"name": "cloud-two",
                  "note": "This is cloud-two"}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(201, resp.status_code)
        self.assertIn('Location', resp.headers)
        self.assertEqual(
            resp.headers['Location'],
            "{}/{}".format(url, resp.json()['id'])
        )
        self.assertEqual("cloud-two", resp.json()['name'])

    def test_create_cloud_with_no_name_fails(self):
        values = {"note": "This is cloud one."}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(resp.status_code, 400)
        err_msg = ["'name' is a required property"]
        self.assertEqual(resp.json()['errors'], err_msg)

    def test_create_cloud_with_duplicate_name_fails(self):
        self.create_cloud("ORD135")

        values = {"name": "ORD135"}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(409, resp.status_code)

    def test_create_region_with_extra_id_property_fails(self):
        values = {"name": "test", "id": 101}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(resp.status_code, 400)
        msg = ["Additional properties are not allowed ('id' was unexpected)"]
        self.assertEqual(resp.json()['errors'], msg)

    def test_create_region_with_extra_created_at_property_fails(self):
        values = {"name": "test", "created_at": "some date"}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(resp.status_code, 400)
        msg = ["Additional properties are not allowed "
               "('created_at' was unexpected)"]
        self.assertEqual(resp.json()['errors'], msg)

    def test_create_region_with_extra_updated_at_property_fails(self):
        values = {"name": "test", "updated_at": "some date"}
        url = self.url + '/v1/clouds'
        resp = self.post(url, data=values)
        self.assertEqual(resp.status_code, 400)
        msg = ["Additional properties are not allowed "
               "('updated_at' was unexpected)"]
        self.assertEqual(resp.json()['errors'], msg)

    def test_clouds_get_all(self):
        self.create_cloud("ORD1")
        self.create_cloud("ORD2")
        url = self.url + '/v1/clouds'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.json()))

    def test_clouds_get_all_with_name_filter(self):
        self.create_cloud("ORD1")
        self.create_cloud("ORD2")
        url = self.url + '/v1/clouds?name=ORD1'
        resp = self.get(url)
        self.assertEqual(200, resp.status_code)
        clouds = resp.json()['clouds']
        self.assertEqual(1, len(clouds))
        self.assertEqual('ORD1', clouds[0]['name'])

    def test_cloud_with_non_existing_filters(self):
        self.create_cloud("ORD1")
        url = self.url + '/v1/clouds?name=idontexist'
        resp = self.get(url)
        self.assertEqual(404, resp.status_code)

    def test_cloud_get_details_for_cloud(self):
        regvars = {"a": "b", "one": "two"}
        cloud = self.create_cloud("ORD1", variables=regvars)
        url = self.url + '/v1/clouds/{}'.format(cloud['id'])
        resp = self.get(url)
        cloud = resp.json()
        self.assertEqual(cloud['name'], 'ORD1')
        self.assertEqual(regvars, cloud['variables'])


class TestPagination(TestCase):

    def setUp(self):
        super(TestPagination, self).setUp()
        self.clouds = [self.create_cloud('cloud-{}'.format(i))
                       for i in range(0, 61)]
        self.addCleanup(self.delete_clouds, self.clouds)

    def test_list_first_thirty_clouds(self):
        url = self.url + '/v1/clouds'
        response = self.get(url)
        self.assertSuccessOk(response)
        json = response.json()
        self.assertIn('clouds', json)
        self.assertEqual(30, len(json['clouds']))
        self.assertListEqual([r['id'] for r in self.clouds[:30]],
                             [r['id'] for r in json['clouds']])

    def test_get_returns_correct_next_link(self):
        url = self.url + '/v1/clouds'
        thirtieth_cloud = self.clouds[29]
        response = self.get(url)
        self.assertSuccessOk(response)
        json = response.json()
        self.assertIn('links', json)
        for link_rel in json['links']:
            if link_rel['rel'] == 'next':
                break
        else:
            self.fail("No 'next' link was returned in response")

        parsed_next = urllib.parse.urlparse(link_rel['href'])
        self.assertIn('marker={}'.format(thirtieth_cloud['id']),
                      parsed_next.query)

    def test_get_returns_correct_prev_link(self):
        first_cloud = self.clouds[0]
        thirtieth_cloud = self.clouds[29]
        url = self.url + '/v1/clouds?marker={}'.format(thirtieth_cloud['id'])
        response = self.get(url)
        self.assertSuccessOk(response)
        json = response.json()
        self.assertIn('links', json)
        for link_rel in json['links']:
            if link_rel['rel'] == 'prev':
                break
        else:
            self.fail("No 'prev' link was returned in response")

        parsed_prev = urllib.parse.urlparse(link_rel['href'])
        self.assertIn('marker={}'.format(first_cloud['id']),
                      parsed_prev.query)
