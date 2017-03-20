"""Module containing generic utilies for Craton."""
from datetime import date
from decorator import decorator
from flask import json, Response
import werkzeug.exceptions

from oslo_log import log

import craton.exceptions as exceptions

LOG = log.getLogger(__name__)


def copy_project_id_into_json(context, json, project_id_key='project_id'):
    """Copy the project_id from the context into the JSON request body.

    :param context:
        The request context object.
    :param json:
        The parsed JSON request body.
    :returns:
        The JSON with the project-id from the headers added as the
        "project_id" value in the JSON.
    :rtype:
        dict
    """
    json[project_id_key] = getattr(context, 'tenant', '')
    return json


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


JSON_KWARGS = {
    "indent": 2,
    "sort_keys": True,
    "cls": JSONEncoder,
    "separators": (",", ": "),
}


def handle_all_exceptions(e):
    headers = [("Content-Type", "application/json")]
    if isinstance(e, exceptions.Base):
        message = e.message
        status = e.code
    elif isinstance(e, werkzeug.exceptions.HTTPException):
        message = e.description
        status = e.code
        headers.extend(
            h for h in e.get_headers(None) if h[0].lower() != "content-type"
        )
    else:
        LOG.exception(e)
        e_ = exceptions.UnknownException
        message = e_.message
        status = e_.code


    body = {
        "message": message,
        "status": status,
    }

    body_ = "{}\n".format(json.dumps(body, **JSON_KWARGS))
    return Response(body_, status, headers)


@decorator
def handle_all_exceptions_decorator(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return handle_all_exceptions(e)
