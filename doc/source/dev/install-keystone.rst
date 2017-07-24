=======================================================
Setting up Craton with Keystone Using OpenStack-Ansible
=======================================================

OpenStack-Ansible is an upstream project that uses Ansible to deploy and
configure production OpenStack from source. It also has the ability to deploy
an environment entirely on one machine like devstack. OpenStack-Ansible
(a.k.a., OSA) refers to these as AIOs (All In One). OSA's `Quick Start`_
documentation describes how to build these.

Once you have an AIO set-up, you need to create the Craton service user, add
the admin role to that user, set up the service and endpoints, and then you
need to do something a little unusual, depending on how you are developing
Craton.

If you have OSA and craton on the same machine, then Craton should be able to
talk to what OSA calls it's "Internal LB VIP". This is usually an IP address
that looks like ``172.29.236.100``. In this case, you should be fine to then
start using Craton with Keystone authentication (assuming you've also followed
the instructions for using Craton with Keystone).

If you do not have them on the same machine, then Craton will not be able to
access the "Internal LB VIP" because (as its name might suggest) it is
internal to that AIO. In that case, you need to use the openstack client to
edit the Admin endpoint for Keystone itself. By default, the admin endpoint
will be something like: ``http://172.29.236.100:35357/v3``. Since we're
talking to Keystone from outside that AIO we need it to be the same as the
public endpoint which will look like ``https://<ip-of-server>:5000/v3``. To
update that, we need to do this:

.. code-block:: bash

    export ADMIN_ENDPOINT_ID="$(openstack endpoint list --service identity \
                                                        --interface admin \
                                                        -c ID \
                                                        -f value)"
    export PUBLIC_URL="$(openstack endpoint list --service identity \
                                                 --interface admin \
                                                 -c URL \
                                                 -f value)"
    openstack endpoint set --region RegionOne \
                           --service identity \
                           --url $PUBLIC_URL \
                           --interface admin \
                           $ADMIN_ENDPOINT_ID

This ensures that ``keystonemiddleware`` will get the public IP address from
the service catalog when it needs to talk to the admin identity endpoint.


.. _Quick Start:
    https://docs.openstack.org/openstack-ansible/latest/contributor/quickstart-aio.html
