import jsonschema

from craton import api
from craton.api.v1.schemas import filters, validators, scopes
from craton.tests import TestCase


class TestAPISchema(TestCase):
    """Confirm that valid schema are defined."""
    pass


def generate_schema_validation_functions(cls):
    def gen_test(name, schema):
        def test(self):
            self.assertIs(
                jsonschema.Draft4Validator.check_schema(schema), None
            )
        setattr(cls, 'test_valid_schema_{}'.format(name), test)

    for (endpoint, method), s in validators.items():
        schema = s.get('args') or s.get('json')
        name = '_'.join(('validator', endpoint, method))
        gen_test(name, schema)

    for (endpoint, method), responses in filters.items():
        for return_code, json in responses.items():
            if json['schema']:
                name = '_'.join(('filter', endpoint, method, str(return_code)))
                gen_test(name, json['schema'])


generate_schema_validation_functions(TestAPISchema)


class TestSchemaLocationInRoute(TestCase):
    def setUp(self):
        super().setUp()
        self.app = api.setup_app()


def generate_endpoint_method_validation_functions(cls):
    def gen_test(test_type, endpoint, method):
        def test(self):
            rules = [
                rule for rule in self.app.url_map.iter_rules()
                if rule.endpoint == endpoint and method in rule.methods
            ]
            self.assertEqual(len(rules), 1)
        test_name = 'test_{}_endpoint_method_in_routes_{}_{}'.format(
            test_type, endpoint, method
        )
        setattr(cls, test_name, test)

    for (_endpoint, method) in validators:
        endpoint = "v1.{}".format(_endpoint)
        gen_test('validators', endpoint, method)

    for (_endpoint, method) in filters:
        endpoint = "v1.{}".format(_endpoint)
        gen_test('filters', endpoint, method)

    for (_endpoint, method) in scopes:
        endpoint = "v1.{}".format(_endpoint)
        gen_test('scopes', endpoint, method)


generate_endpoint_method_validation_functions(TestSchemaLocationInRoute)
