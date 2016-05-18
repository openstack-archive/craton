import os
import sys
from wsgiref import simple_server

from oslo_config import cfg
from oslo_log import log as logging

from craton.inventory import api

LOG = logging.getLogger(__name__)

CONF = cfg.CONF


def main():
    logging.register_options(CONF)
    CONF(sys.argv[1:],
         project='craton-inventory',
         default_config_files=[])
    logging.setup(CONF, 'craton-inventory')

    app = api.load_app()
    host, port = cfg.CONF.api.host, cfg.CONF.api.port
    srv = simple_server.make_server(host, port, app)
    LOG.info("Starting API server in PID: %s" % os.getpid())
    srv.serve_forever()


if __name__ == "__main__":
    main()
