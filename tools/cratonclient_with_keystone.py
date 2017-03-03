"""An example usage of cratonclient when working with Craton and Keystone.

Requires:

    - Craton to be configured using Keystone for identity (configuring
      etc/craton-api-conf.sample [keystone_authtoken] section and
      etc/craton-api-paste.ini to use keystoneauthcontext)

      etc/craton-api-conf.sample should include something that looks like:

      .. code-block:: ini

            # etc/craton-api-conf.sample
            [keystone_authtoken]
            auth_host = 127.0.0.1
            auth_port = 5000
            auth_version = 3
            auth_protocol = http
            project_name = service
            username = craton
            password = craton
            project_domain_id = default
            user_domain_id = default
            auth_type = password

      While etc/craton-api.paste.ini should include something that looks like:

      .. code-block:: ini

            [pipeline:main]
            pipeline = request_id keystonecontext api_v1

    - Installing python-cratonclient

"""

from keystoneauth1.identity.v3 import password as password_auth
from keystoneauth1 import session as ksa_session

from cratonclient import session
from cratonclient.v1 import client

KEYSTONE_DOMAIN = '127.0.0.1'
KEYSTONE_PORT = '5000'
USERNAME = 'admin'
PASSWORD = 'secretepassword'
PROJECT_NAME = 'admin'
PROJECT_DOMAIN_NAME = 'Default'
USER_DOMAIN_NAME = 'Default'
AUTH_URL = 'http://{domain}:{port}/v3'.format(domain=KEYSTONE_DOMAIN,
                                              port=KEYSTONE_PORT)


admin_auth = password_auth.Password(
    auth_url=AUTH_URL,
    password=PASSWORD,
    username=USERNAME,
    user_domain_name=USER_DOMAIN_NAME,
    project_name=PROJECT_NAME,
    project_domain_name=PROJECT_DOMAIN_NAME,
)
craton_session = session.Session(
    session=ksa_session.Session(auth=admin_auth,
                                verify=False),
)
craton = client.Client(
    session=craton_session,
    url='http://127.0.0.1:7780/',
)

inventory = craton.inventory(1)
hosts = inventory.hosts.list()
