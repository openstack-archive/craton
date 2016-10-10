"""Tests for craton.util module."""

from craton import tests
from craton import util


class TestProjectIdUtilities(tests.TestCase):
    """Unit tests for the copy_project_id_into_json function."""

    def test_adds_project_id_to_json(self):
        """Verify we add the project_id to the json body."""
        self.context.tenant = '1'
        json = util.copy_project_id_into_json(self.context, {})
        self.assertDictEqual({'project_id': 1}, json)

    def test_defaults_project_id_to_zero(self):
        """Verify if there's no tenant attribute on the context we use 0."""
        del self.context.tenant
        json = util.copy_project_id_into_json(self.context, {})
        self.assertDictEqual({'project_id': 0}, json)

    def test_tries_to_convert_projects_to_integers(self):
        """Verify it raises ValueErrors on non-integer tenants."""
        try:
            util.copy_project_id_into_json(self.context, {})
        except ValueError:
            return
        else:
            self.fail("Expected craton.util.copy_project_id_to_json to raise"
                      " a ValueError but it did not.")
