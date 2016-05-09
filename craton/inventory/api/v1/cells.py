from flask import request, g
from oslo_serialization import jsonutils

from craton.inventory.api.v1 import base
from craton.inventory import db as dbapi

class Cells(base.Resource):

    def get(self):
        region =  g.args["region"]
        cell = g.args["name"]
        context = request.environ.get('context')

        if region == 'None' and cell == 'None':
            cells = dbapi.cells_get_all(context)
            response = jsonutils.to_primitive(cells)
            return response, 200, None
        else:
            filters = {}
            if region != 'None':
                filters['region'] =  region
            if cell != 'None':
                filters['name'] = cell

            cells = dbapi.cells_get_by_filters(context, filters)
            response = jsonutils.to_primitive(cells)
            return response, 200, None


    def post(self):
        print "cells post"
        print g.json

        return None, 200, None


class CellsId(base.Resource):

    def put(self, id):
        print "cells id put"
        print g.json
        return None, 405, None

    def delete(self, id):

        return None, 400, None


class CellsData(base.Resource):

    def put(self, id):
        print "cells data put"
        print g.json

        return None, 400, None

    def delete(self, id):

        return None, 400, None
