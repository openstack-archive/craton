import os
from paste import deploy
from flask import Flask


from oslo_config import cfg
from oslo_log import log as logging

from craton.api import v1


LOG = logging.getLogger(__name__)

api_opts = [
    cfg.StrOpt('api_paste_config',
               default="api-paste.ini",
               help="Configuration file for API service."),
    cfg.StrOpt('paste_pipeline',
               default="local-auth",
               choices=["local-auth", "keystone-auth"],
               help="""\
The name of the Paste pipeline to use for Craton.

Pipelines are organized according to authentication scheme. The available
choices are:

- ``local-auth`` (the default) Uses Craton's default authentication and
  authorization scheme
- ``keystone-auth`` Uses Keystone for identity, authentication, and
  authorization
"""),
    cfg.StrOpt('host',
               default="127.0.0.1",
               help="API host IP"),
    cfg.IntOpt('port',
               default=5000,
               help="API port to use.")
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='api',
                         title='Craton API service group options')
CONF.register_group(opt_group)
CONF.register_opts(api_opts, opt_group)


def create_app(global_config, **local_config):
    return setup_app()


def setup_app(config=None):
    app = Flask(__name__, static_folder=None)
    app.config.update(
        PROPAGATE_EXCEPTIONS=True
    )
    app.register_blueprint(v1.bp, url_prefix='/v1')
    return app


def load_app():
    cfg_file = None
    cfg_path = CONF.api.api_paste_config
    paste_pipeline = CONF.api.paste_pipeline
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([cfg.CONF.api.api_paste_config])
    LOG.info("Loading craton-api with pipeline %(pipeline)s and WSGI config:"
             "%(conf)s", {'conf': cfg_file, 'pipeline': paste_pipeline})
    return deploy.loadapp("config:%s" % cfg_file, name=paste_pipeline)
