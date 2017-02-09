from craton import api
from craton.tests import TestCase


class TestRouteURLNaming(TestCase):
    pass


def generate_route_naming_functions(cls):
    def gen_test(endpoint, url):
        def test(self):
            pattern = (
                "^/v1/([a-z-]+|<any\('[a-z-]+'(, '[a-z-]+')*\):resources>)"
                "(/<id>(/[a-z-]+)?)?"
            )
            self.assertRegex(url, pattern)
        test_name = 'test_route_naming_{}'.format(endpoint)
        setattr(cls, test_name, test)

    app = api.setup_app()
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint[3:]
        url = rule.rule
        gen_test(endpoint, url)


generate_route_naming_functions(TestRouteURLNaming)
