from craton import api
from craton.tests import TestCase


class TestRouteURLNaming(TestCase):
    pass


def generate_route_naming_functions(cls):
    def gen_test(endpoint, url):
        def test(self):
            self.assertRegex(url, '^/v1/[a-z-]+(/<id>(/[a-z-]+)?)?$')
        test_name = 'test_route_naming_{}'.format(endpoint)
        setattr(cls, test_name, test)

    app = api.setup_app()
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint[3:]
        url = rule.rule
        gen_test(endpoint, url)


generate_route_naming_functions(TestRouteURLNaming)
