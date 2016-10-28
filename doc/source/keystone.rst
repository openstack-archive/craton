===========================
Using Keystone for Identity
===========================

By default, Craton uses it's own local authentication mechanism. It also
supports using Keystone for identity and authentication.

Before you can proceed, you need to first create a user for Craton, e.g.,

.. code-block:: bash

    openstack user create --project service \
                          --description 'Craton Service User' \
                          --password-prompt \
                          --enable \
                          craton

And then you must add the admin role to it:

.. code-block:: bash

    openstack role add --user craton \
                       --project service \
                       admin

And then you must create the service and endpoints:

.. code-block:: bash

    openstack service create --description 'Craton Fleet Management' \
                             --name 'craton' \
                             --enable \
                             fleet_management
    for endpoint_type in "admin internal public" ; do
      openstack endpoint create \
        fleet_management $endpoint_type http://<ip>:<port>/v1 \
        --region RegionOne
    done

Then you need to select the ``keystone-auth`` pipeline and configure the usual
Keystone auth token middleware options in the Craton API config file, e.g.,

.. code-block:: ini

    [api]
    # ...
    paste_pipeline = keystone-auth

    [keystone_authtoken]
    auth_uri = https://<keystone-ip>:5000
    auth_url = https://<keystone-ip>:35357/v3
    project_name = service
    username = craton
    password = aVery_Secure&Complex+Password
    project_domain_id = default
    user_domain_id = default
    auth_type = password

You may need to either not use ``https`` in your URL or set ``insecure =
True`` to avoid SSL errors.

Now with an appropriate identity in Keystone, one can use either the python
craton client or another client that can retrieve tokens from Keystone. For
example, if you use the openstack client to grab a token, you can use curl to
talk to Craton:

.. code-block:: bash

    export AUTH_TOKEN="$(openstack token issue -c id -f value)"
    curl -i \
         -H"X-Auth-Token: $AUTH_TOKEN" \
         http://<ip>:<port>/v1/hosts?region_id=1
