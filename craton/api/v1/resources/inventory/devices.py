from oslo_serialization import jsonutils
from oslo_log import log

from craton.api.v1 import base
from craton.api.v1.resources import utils
from craton import exceptions
from craton import db as dbapi
from craton.db.sqlalchemy import models


LOG = log.getLogger(__name__)


class Devices(base.Resource):

    @base.http_codes
    @base.pagination_context
    def get(self, context, request_args, pagination_params):
        """Get all devices, with optional filtering."""
        details = request_args.get("details")
        device_objs, link_params = dbapi.devices_get_all(
            context, request_args, pagination_params,
        )
        links = base.links_from(link_params)

        devices = {"hosts": [], "network-devices": []}
        for device_obj in device_objs:
            if details:
                device = utils.get_resource_with_vars(request_args,
                                                      device_obj)
            else:
                device = jsonutils.to_primitive(device_obj)

            utils.add_up_link(context, device)

            if isinstance(device_obj, models.Host):
                devices["hosts"].append(device)
            elif isinstance(device_obj, models.NetworkDevice):
                devices["network-devices"].append(device)
            else:
                LOG.error(
                    "The device is of unknown type: '%s'", device_obj
                )
                raise exceptions.UnknownException

        response_body = jsonutils.to_primitive(
            {'devices': devices, 'links': links}
        )

        return response_body, 200, None
