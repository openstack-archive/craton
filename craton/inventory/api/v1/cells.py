from flask import request, g
from craton.inventory.api.v1 import base
#from . import schemas


class Cells(base.Resource):

    def get(self):
        print "cells get"
        print g.args

        return [], 200, None

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
