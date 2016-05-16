# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import g

from craton.inventory.api.v1 import base


class Hosts(base.Resource):

    def get(self):
        print(g.args)

        return [], 200, None

    def post(self):
        print(g.json)

        return None, 200, None


class HostsId(base.Resource):

    def put(self, id):
        print(g.json)

        return None, 400, None

    def delete(self, id):

        return None, 400, None


class HostsData(base.Resource):

    def put(self, id):
        print(g.json)

        return None, 400, None

    def delete(self, id):

        return None, 400, None
