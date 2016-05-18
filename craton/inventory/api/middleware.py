from oslo_middleware import base
from oslo_middleware import request_id
from oslo_context import context

import flask
from flask import request


class ContextMiddleware(base.Middleware):

    def make_context(self, request, *args, **kwargs):
        req_id = request.environ.get(request_id.ENV_REQUEST_ID)
        kwargs.setdefault('request_id', req_id)

        # TODO(sulo): Insert Craton specific context here if needed,
        # for now we are using generic context object.
        ctxt = context.RequestContext(*args, **kwargs)
        request.environ['context'] = ctxt
        return ctxt


class NoAuthContextMiddleware(ContextMiddleware):

    def __init__(self, application):
        self.application = application

    def process_request(self, request):
        # Simply insert some dummy context info
        self.make_context(
            request,
            auth_token='noauth-token',
            user='noauth-user',
            tenant=1,
        )

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(application):
            return cls(application)

        return _factory


class LocalAuthContextMiddleware(ContextMiddleware):

    def __init__(self, application):
        self.applicatin = application

    def process_request(self, request):
        # TODO(sulo): for local auth we simply check pre-defined APIkey
        # ProjectID and UserID against the db here and proceed accordingly.
        headers = request.headers
        self.make_context(
            request,
            auth_token=headers.get('X-Auth-Token', None),
            user=headers.get('X-Auth-User', None),
            tenant=headers.get('X-Auth-Project', None)
        )

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app)
        return _factory


class KeystoneAuthContextMiddleware(ContextMiddleware):

    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        with self._app.request_context(environ):
            self.process_request(request)
        return self._app(environ, start_response)

    def process_request(self, request):
        headers = request.headers

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
        def _factory(app):
            return cls(app)
        return _factory
