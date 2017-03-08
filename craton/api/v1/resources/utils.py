import binascii
import os
from flask import url_for
from oslo_serialization import jsonutils

from craton import db as dbapi


def format_variables(args, obj):
    """Update resource response with requested type of variables."""
    if args:
        resolved_values = args.get("resolved-values", None)
    else:
        resolved_values = None

    if resolved_values:
        obj.vars = obj.resolved
    else:
        obj.vars = obj.variables
    return obj


def get_resource_with_vars(args, obj):
    """Get resource in json primitive with variables."""
    obj = format_variables(args, obj)
    res = jsonutils.to_primitive(obj)
    res['variables'] = jsonutils.to_primitive(obj.vars)
    return res


def get_device_type(context, device_id):
    device = dbapi.resource_get_by_id(context, "devices", device_id)
    return device.type


def get_resource_url(resource_type, resource_id):
    resources = {
        "cells": "v1.cells_id",
        "hosts": "v1.hosts_id",
        "network_devices": "v1.network_devices_id",
        "regions": "v1.regions_id",
    }
    return url_for(resources[resource_type], id=resource_id, _external=True)


def add_up_link(context, device):
    if device["parent_id"]:
        device_type = get_device_type(context, device["parent_id"])
        link_url = get_resource_url(device_type, device["parent_id"])
    elif device["cell_id"]:
        link_url = get_resource_url("cells", device["cell_id"])
    else:
        link_url = get_resource_url("regions", device["region_id"])

    link = {
        "href": link_url,
        "rel": "up",
    }

    links = device.setdefault("links", [])
    links.append(link)


def gen_api_key():
    """Generates crypto strong 16 bytes api key."""
    # NOTE(sulo): this implementation is taken from secrets
    # moudule available in python 3.6
    tbytes = os.urandom(16)
    return binascii.hexlify(tbytes).decode('ascii')
