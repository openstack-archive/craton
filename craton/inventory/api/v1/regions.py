from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.inventory.api.v1 import base
from craton.inventory import db as dbapi
from craton.inventory import exceptions


LOG = log.getLogger(__name__)


class Regions(base.Resource):

    def get(self, id=None):
        """Get region(s) for the project. Get region details if
        for a particular region.
        """
        # region_id =  g.args["id"]
        # region_name = g.args["name"]
        region_id = id or 'None'
        region_name = 'None'
        context = request.environ.get('context')

        if region_id == 'None' and region_name == 'None':
            # Get all regions for this tenant
            try:
                regions_obj = dbapi.regions_get_all(context)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if regions_obj:
                result = jsonutils.to_primitive(regions_obj)
                return result, 200, None
            else:
                return None, 404, None

        if region_name != 'None':
            try:
                region_obj = dbapi.regions_get_by_name(context, region_name)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if region_obj:
                region_obj.data = region_obj.variables
                result = jsonutils.to_primitive(region_obj)
                return result, 200, None
            else:
                return None, 404, None

        if region_id != 'None':
            try:
                region_obj = dbapi.regions_get_by_id(context, region_id)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if region_obj:
                region_obj.data = region_obj.variables
                result = jsonutils.to_primitive(region_obj)
                return result, 200, None
            else:
                return None, 404, None

    def post(self):
        """Create a new region."""
        context = request.environ.get('context')
        try:
            dbapi.regions_create(context, g.json)
        except Exception as err:
            LOG.error("Error during region create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def put(self, id):
        """Update existing region."""
        # NOTE(sulo): we can only update `note` on region
        return None, 200, None

    def delete(self, id):
        """Delete existing region."""
        context = request.environ.get('context')
        try:
            dbapi.regions_delete(context, id)
        except Exception as err:
            LOG.error("Error during region delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None


class RegionsData(base.Resource):

    def put(self, id):
        """
        Update existing region data, or create if it does
        not exist.
        """
        data_keys = request.form.keys()
        data = dict((key, request.form.getlist(key)[0]) for key in data_keys)
        context = request.environ.get('context')
        try:
            dbapi.regions_data_update(context, id, data)
        except Exception as err:
            LOG.error("Error during region data update: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def delete(self, id):
        """Delete region data."""
        # NOTE(sulo): this is not that great. Find a better way to do this.
        # We can pass multiple keys suchs as key1=one key2=two etc. but not
        # the best way to do this.
        data_keys = request.form.keys()
        data = dict((key, request.form.getlist(key)[0]) for key in data_keys)
        context = request.environ.get('context')
        try:
            dbapi.regions_data_delete(context, id, data)
        except Exception as err:
            LOG.error("Error during region delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
