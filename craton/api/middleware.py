from oslo_middleware import base
from oslo_middleware import request_id
from oslo_context import context
from oslo_log import log
from oslo_utils import uuidutils

import flask
from flask import request
import json

from craton.db import api as dbapi
from craton import exceptions


LOG = log.getLogger(__name__)


class ContextMiddleware(base.Middleware):

    def make_context(self, request, *args, **kwargs):
        req_id = request.environ.get(request_id.ENV_REQUEST_ID)
        kwargs.setdefault('request_id', req_id)

        # TODO(sulo): Insert Craton specific context here if needed,
        # for now we are using generic context object.
        ctxt = context.RequestContext(*args, **kwargs)
        request.environ['context'] = ctxt
        return ctxt

    def _invalid_project_id(self, project_id):
        err_msg = json.dumps({
            "message": "Project ID ('{}') is not a valid UUID".format(
                project_id)
        })
        return flask.Response(response=err_msg, status=401,
                              headers={'Content-Type': 'application/json'})


class NoAuthContextMiddleware(ContextMiddleware):

    def __init__(self, application):
        self.application = application

    def process_request(self, request):
        # Simply insert some dummy context info
        self.make_context(
            request,
            auth_token='noauth-token',
            user='noauth-user',
            tenant=None,
            is_admin=True,
            is_admin_project=True,
        )

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(application):
            return cls(application)

        return _factory


class LocalAuthContextMiddleware(ContextMiddleware):

    def __init__(self, application):
        self.application = application

    def process_request(self, request):
        headers = request.headers
        project_id = headers.get('X-Auth-Project')
        if not uuidutils.is_uuid_like(project_id):
            return self._invalid_project_id(project_id)

        ctx = self.make_context(
            request,
            auth_token=headers.get('X-Auth-Token', None),
            user=headers.get('X-Auth-User', None),
            tenant=project_id,
            )

        # NOTE(sulo): this means every api call hits the db
        # at least once for auth. Better way to handle this?
        try:
            user_info = dbapi.get_user_info(ctx,
                                            headers.get('X-Auth-User', None))
            if user_info.api_key != headers.get('X-Auth-Token', None):
                return flask.Response(status=401)
            if user_info.is_root:
                ctx.is_admin = True
                ctx.is_admin_project = True
            elif user_info.is_admin:
                ctx.is_admin = True
                ctx.is_admin_project = False
            else:
                ctx.is_admin = False
                ctx.is_admin_project = False
        except exceptions.NotFound:
            return flask.Response(status=401)
        except Exception as err:
            LOG.error(err)
            return flask.Response(status=500)

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(application):
            return cls(application)
        return _factory


class KeystoneAuthContextMiddleware(ContextMiddleware):

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        with self.application.request_context(environ):
            self.process_request(request)
        return self.application(environ, start_response)

    def process_request(self, request):
        headers = request.headers
        project_id = headers.get('X-Auth-Project')
        if not uuidutils.is_uuid_like(project_id):
            return self._invalid_project_id(project_id)

        try:
            if headers["X-Identity-Status"] == "Invalid":
                return flask.Response(status=401)
        except KeyError:
            # See: keystone middleware #exchanging-user-information
            pass

        project_id = headers.get('X-Project-ID')
        if project_id is None:
            return flask.Response(status=401)

        self.make_context(
            request,
            auth_token=headers.get('X-Auth-Token'),
            user=headers.get('X-User-ID'),
            tenant=project_id,
        )

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(application):
            return cls(application)
        return _factory
