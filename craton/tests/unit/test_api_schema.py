import jsonschema

from craton import api
from craton.api.v1.schemas import filters, validators
from craton.tests import TestCase


VALIDATORS = {
    "with_schema": [
        ('ansible_inventory', 'GET'),
        ('cells', 'GET'),
        ('cells', 'POST'),
        ('cells_id', 'GET'),
        ('cells_id', 'PUT'),
        ('hosts', 'GET'),
        ('hosts', 'POST'),
        ('hosts_id', 'GET'),
        ('hosts_id', 'PUT'),
        ('hosts_labels', 'DELETE'),
        ('hosts_labels', 'GET'),
        ('hosts_labels', 'PUT'),
        ('network_devices', 'GET'),
        ('network_devices', 'POST'),
        ('network_devices_id', 'GET'),
        ('network_devices_id', 'PUT'),
        ('network_devices_labels', 'GET'),
        ('network_devices_labels', 'PUT'),
        ('network_devices_labels', 'DELETE'),
        ('network_interfaces', 'GET'),
        ('network_interfaces', 'POST'),
        ("network_interfaces_id", "GET"),
        ('network_interfaces_id', 'PUT'),
        ('networks', 'GET'),
        ('networks', 'POST'),
        ("networks_id", "GET"),
        ('networks_id', 'PUT'),
        ('projects', 'GET'),
        ('projects', 'POST'),
        ("projects_id", "GET"),
        ('projects_id_variables', 'GET'),
        ('projects_id_variables', 'PUT'),
        ('projects_id_variables', 'DELETE'),
        ('regions', 'GET'),
        ('regions', 'POST'),
        ("regions_id", "GET"),
        ('regions_id', 'PUT'),
        ('users', 'GET'),
        ('users', 'POST'),
        ("users_id", "GET"),
        ('variables_with_resolve', 'DELETE'),
        ('variables_with_resolve', 'GET'),
        ('variables_with_resolve', 'PUT'),
        ('variables_without_resolve', 'DELETE'),
        ('variables_without_resolve', 'GET'),
        ('variables_without_resolve', 'PUT'),
    ],
    "without_schema": [
        ('cells_id', 'DELETE'),
        ('hosts_id', 'DELETE'),
        ('network_devices_id', 'DELETE'),
        ("network_interfaces_id", "DELETE"),
        ("networks_id", "DELETE"),
        ("projects_id", "DELETE"),
        ("users_id", "DELETE"),
        ("regions_id", "DELETE"),
    ]
}


class TestAPISchema(TestCase):
    """Confirm that valid schema are defined."""
    def test_all_validators_have_test(self):
        known = set(VALIDATORS["with_schema"] + VALIDATORS["without_schema"])
        defined = set(validators.keys())
        self.assertSetEqual(known, defined)


def generate_schema_validation_functions(cls):
    def gen_validator_schema_test(endpoint, method):
        def test(self):
            try:
                loc_schema = validators[(endpoint, method)]
            except KeyError:
                self.fail(
                    'The validator {} is missing from the schemas '
                    'validators object.'.format((endpoint, method))
                )

            self.assertEqual(len(loc_schema), 1)
            locations = {
                'GET': 'args',
                'DELETE': 'json',
                'PUT': 'json',
                'POST': 'json',
            }
            location, schema = loc_schema.popitem()
            self.assertIn(method, locations)
            self.assertEqual(locations[method], location)
            self.assertIs(
                jsonschema.Draft4Validator.check_schema(schema), None
            )
            if 'type' not in schema or schema['type'] == 'object':
                self.assertFalse(schema['additionalProperties'])

        name = '_'.join(('validator', endpoint, method))
        setattr(cls, 'test_valid_schema_{}'.format(name), test)

    for (endpoint, method) in VALIDATORS["with_schema"]:
        gen_validator_schema_test(endpoint, method)

    def gen_no_validator_schema_test(endpoint, method):
        def test(self):
            try:
                loc_schema = validators[(endpoint, method)]
            except KeyError:
                self.fail(
                    'The validator {} is missing from the schemas '
                    'validators object.'.format((endpoint, method))
                )
            self.assertEqual({}, loc_schema)
        name = '_'.join(('validator', endpoint, method))
        setattr(cls, 'test_no_schema_{}'.format(name), test)

    for (endpoint, method) in VALIDATORS["without_schema"]:
        gen_no_validator_schema_test(endpoint, method)

    def gen_filter_test(name, schema):
        def test(self):
            self.assertIs(
                jsonschema.Draft4Validator.check_schema(schema), None
            )
            if 'type' not in schema or schema['type'] == 'object':
                self.assertFalse(schema['additionalProperties'])
        setattr(cls, 'test_valid_schema_{}'.format(name), test)

    for (endpoint, method), responses in filters.items():
        for return_code, json in responses.items():
            if json['schema']:
                name = '_'.join(('filter', endpoint, method, str(return_code)))
                gen_filter_test(name, json['schema'])


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


generate_endpoint_method_validation_functions(TestSchemaLocationInRoute)


class TestRoutesInValidators(TestCase):
    pass


def generate_route_validation_functions(cls):
    def gen_test(test_type, checker, endpoint, method):
        def test(self):
            self.assertIn((endpoint, method), checker)
        test_name = 'test_route_in_{}_{}_{}'.format(
            test_type, endpoint, method
        )
        setattr(cls, test_name, test)

    app = api.setup_app()
    for rule in app.url_map.iter_rules():
        # remove 'v1.' from start of endpoint
        endpoint = rule.endpoint[3:]
        for method in rule.methods:
            if method == 'OPTIONS':
                continue
            elif method == 'HEAD' and 'GET' in rule.methods:
                continue
            else:
                gen_test('validators', validators, endpoint, method)
                gen_test('filters', filters, endpoint, method)


generate_route_validation_functions(TestRoutesInValidators)
