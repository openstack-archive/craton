from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton.api.v1 import utils
from craton import db as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class Regions(base.Resource):

    def get(self, id=None):
        """Get region(s) for the project. Get region details if
        for a particular region.
        """
        _id = g.args["id"]
        _name = g.args["name"]
        region_id = id or _id
        region_name = _name
        filters = {}
        filters["var_filters"] = utils.extract_variable_filters()

        context = request.environ.get('context')

        if not region_id and not region_name:
            # Get all regions for this tenant
            try:
                regions_obj = dbapi.regions_get_all(context, filters)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if regions_obj:
                result = jsonutils.to_primitive(regions_obj)
                return result, 200, None
            else:
                return None, 404, None

        if region_name:
            try:
                region_obj = dbapi.regions_get_by_name(context, region_name)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if region_obj:
                region_obj.data = region_obj.variables
                result = jsonutils.to_primitive(region_obj)
                return [result], 200, None
            else:
                return None, 404, None

        if region_id:
            try:
                region_obj = dbapi.regions_get_by_id(context, region_id)
            except exceptions.NotFound:
                return self.error_response(404, 'Not Found')

            if region_obj:
                region_obj.data = region_obj.variables
                result = jsonutils.to_primitive(region_obj)
                return [result], 200, None
            else:
                return None, 404, None

    def post(self):
        """Create a new region."""
        context = request.environ.get('context')
        try:
            region_obj = dbapi.regions_create(context, g.json)
        except Exception as err:
            LOG.error("Error during region create: %s" % err)
            return self.error_response(500, 'Unknown Error')

        region = jsonutils.to_primitive(region_obj)
        return region, 200, None


class RegionsById(base.Resource):

    def get(self, id):
        context = request.environ.get('context')
        try:
            region_obj = dbapi.regions_get_by_id(context, id)
        except exceptions.NotFound:
            return self.error_response(404, 'Not Found')
        except Exception as err:
            LOG.error("Error during Region get by id: %s" % err)
            return self.error_response(500, 'Unknown Error')

        region_obj.data = region_obj.variables
        region = jsonutils.to_primitive(region_obj)
        return region, 200, None

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
        context = request.environ.get('context')
        try:
            dbapi.regions_data_update(context, id, request.json)
        except Exception as err:
            LOG.error("Error during region data update: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None

    def delete(self, id):
        """Delete region data."""
        context = request.environ.get('context')
        try:
            dbapi.regions_data_delete(context, id, request.json)
        except Exception as err:
            LOG.error("Error during region delete: %s" % err)
            return self.error_response(500, 'Unknown Error')

        return None, 200, None
