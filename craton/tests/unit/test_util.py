"""Tests for craton.util module."""
import uuid

from craton import tests
from craton import util


class TestProjectIdUtilities(tests.TestCase):
    """Unit tests for the copy_project_id_into_json function."""

    def test_adds_project_id_to_json(self):
        """Verify we add the project_id to the json body."""
        project_id = uuid.uuid4().hex
        self.context.tenant = project_id
        json = util.copy_project_id_into_json(self.context, {})
        self.assertDictEqual({'project_id': project_id}, json)

    def test_defaults_project_id_to_zero(self):
        """Verify if there's no tenant attribute on the context we use 0."""
        del self.context.tenant
        json = util.copy_project_id_into_json(self.context, {})
        self.assertDictEqual({'project_id': ''}, json)
