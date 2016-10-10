from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton import db as dbapi
from craton import util


LOG = log.getLogger(__name__)


class Regions(base.Resource):

    @base.http_codes
    def get(self, id=None):
        """Get region(s) for the project. Get region details if
        for a particular region.
        """
        _id = g.args["id"]
        _name = g.args["name"]
        region_id = id or _id
        region_name = _name
        context = request.environ.get('context')

        if not region_id and not region_name:
            # Get all regions for this tenant
            regions_obj = dbapi.regions_get_all(context)
            return jsonutils.to_primitive(regions_obj), 200, None

        if region_name:
            region_obj = dbapi.regions_get_by_name(context, region_name)
            region_obj.data = region_obj.variables
            return jsonutils.to_primitive([region_obj]), 200, None

        if region_id:
            region_obj = dbapi.regions_get_by_id(context, region_id)
            region_obj.data = region_obj.variables
            return jsonutils.to_primitive([region_obj]), 200, None

    @base.http_codes
    def post(self):
        """Create a new region."""
        context = request.environ.get('context')
        json = util.copy_project_id_into_json(context, g.json)
        region_obj = dbapi.regions_create(context, json)
        return jsonutils.to_primitive(region_obj), 200, None


class RegionsById(base.Resource):

    @base.http_codes
    def get(self, id):
        context = request.environ.get('context')
        region_obj = dbapi.regions_get_by_id(context, id)
        region_obj.data = region_obj.variables
        return jsonutils.to_primitive(region_obj), 200, None

    def put(self, id):
        """Update existing region."""
        # NOTE(sulo): we can only update `note` on region
        return None, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete existing region."""
        context = request.environ.get('context')
        dbapi.regions_delete(context, id)
        return None, 204, None


class RegionsData(base.Resource):

    @base.http_codes
    def put(self, id):
        """
        Update existing region data, or create if it does
        not exist.
        """
        context = request.environ.get('context')
        dbapi.regions_data_update(context, id, request.json)
        return None, 200, None

    @base.http_codes
    def delete(self, id):
        """Delete region data."""
        context = request.environ.get('context')
        dbapi.regions_data_delete(context, id, request.json)
        return None, 204, None
