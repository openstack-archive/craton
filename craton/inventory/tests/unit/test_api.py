import mock

from craton.inventory.tests import TestCase


class APIV1CellsTest(TestCase):
    def test_get_cells(self):
        pass

    def test_get_cells_with_name(self):
        pass

    def test_get_cell_no_exist_by_name_fails(self):
        pass

    def test_get_cell_by_user_data(self):
        pass

    def test_post_cells_with_valid_data(self):
        pass

    def test_post_cells_with_invalid_data_fails(self):
        pass

    def test_update_cell_no_exist_fails(self):
        pass

    def test_delete_cell_no_exist_fails(self):
        pass


class APIV1RegionsTest(TestCase):
    def test_get_regions(self):
        pass

    def test_get_region_by_name(self):
        pass

    def test_get_region_no_exist_by_name_fails(self):
        pass

    def test_get_region_by_user_data(self):
        pass

    def test_post_region_with_valid_data(self):
        pass

    def test_post_region_with_invalid_data_fails(self):
        pass

    def test_delete_region_no_exist_fails(self):
        pass


class APIV1HostsTest(TestCase):
    def test_get_hosts(self):
        pass

    def test_get_host_by_name(self):
        pass

    def test_get_host_by_ip_address(self):
        pass

    def test_get_host_by_filter_query(self):
        pass

    def test_get_host_no_exist_fails(self):
        pass
