import jsonschema

from craton.api.v1.schemas import filters, validators
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
        schema = s.get('json', s)
        name = '_'.join(('validator', endpoint, method))
        gen_test(name, schema)

    for (endpoint, method), responses in filters.items():
        for return_code, json in responses.items():
            if json['schema']:
                name = '_'.join(('filter', endpoint, method, str(return_code)))
                gen_test(name, json['schema'])


generate_schema_validation_functions(TestAPISchema)
