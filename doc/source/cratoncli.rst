
==================================
Craton service command-line client
==================================

.. program:: craton

Contents
^^^^^^^^

`craton usage`_

`craton optional arguments`_

`craton project-create`_

`craton project-delete`_

`craton project-list`_

`craton project-show`_

`craton project-update`_

`craton region-create`_

`craton region-delete`_

`craton region-list`_

`craton region-show`_

`craton region-update`_

`craton cell-create`_

`craton cell-delete`_

`craton cell-list`_

`craton cell-show`_

`craton cell-update`_

`craton device-create`_

`craton device-delete`_

`craton device-list`_

`craton device-show`_

`craton device-update`_

`craton host-create`_

`craton host-delete`_

`craton host-list`_

`craton host-show`_

`craton host-update`_

`craton user-list`_


craton usage
------------

**Subcommands:**

:program:`craton usage`
    Show usages of craton client.

:program:`craton project-create`
    Create a new project.

:program:`craton project-delete`
    Delete a project.

:program:`craton project-list`
    List all projects.

:program:`craton project-show`
    Show detailed information about a project.

:program:`craton project-update`
    Update information about a project.

:program:`craton region-create`
    Create a new region.

:program:`craton region-delete`
    Delete a region.

:program:`craton region-list`
    List all regions.

:program:`craton region-show`
    Show detailed information about a region.

:program:`craton region-update`
    Update information about a region.

:program:`craton cell-create`
    Create a new cell.

:program:`craton cell-delete`
    Delete a cell.

:program:`craton cell-list`
    List all cells.

:program:`craton cell-show`
    Show detailed information about a cell.

:program:`craton cell-update`
    Update information about a cell.

:program:`craton device-create`
    Create a new device.

:program:`craton device-delete`
    Delete a device.

:program:`craton device-list`
    List all devices.

:program:`craton device-show`
    Show detailed information about a device.

:program:`craton device-update`
    Update information about a device.

:program:`craton host-create`
    Create a new host.

:program:`craton host-delete`
    Delete a host.

:program:`craton host-list`
    List all hosts.

:program:`craton host-show`
    Show detailed information about a host.

:program:`craton host-update`
    Update information about a host.

:program:`craton user-list`
    List the users of a project.

:program:`craton help`
    Display help about this program or one of its subcommands.


craton optional arguments
-------------------------

.. option:: --version

    Show program's version number and exit.

.. option:: -v, --verbose

    Print more verbose output.

craton project-create
---------------------

.. program:: craton project-create

Create a new project.

::

    usage: craton project-create [-n <name>] [-u <uuid>]

**Optional arguments:**

.. option:: -n <name>, --name <name>

    Name of the project.

.. option:: -u <uuid>, --uuid <uuid>

    UUID of the project.


craton project-delete
---------------------

.. program:: craton project-delete

Delete a project.

::

    usage: craton project-delete <project>

**Positional arguments:**

.. option:: project

    UUID of the project.


craton project-list
-------------------

.. program:: craton project-list

List the projects.

::

    usage: craton project-list [--detail] [--limit <limit>]

**Optional arguments:**

.. option:: --detail

    Show detailed information about the projects.

.. option:: --limit <limit>

    Maximum number of projects to return per request, 0 for no limit. Default
    is the maximum number used by the Craton API Service.


craton project-show
-------------------

.. program:: craton project-show

Show detailed information about a project.

::

    usage: craton project-show <project>

**Positional arguments:**

.. option:: project

    UUID of the project.


craton project-update
---------------------

.. program:: craton project-update

Update information about a project.

::

    usage: craton project-update <project> [-n <name>]

**Positional arguments:**

.. option:: project

    UUID of the project.

**Optional arguments:**

.. option:: -n <name>, --name <name>

    New name for the project.

craton region-create
--------------------

.. program:: craton region-create

Create a new region.

::

    usage: craton region-create [-n <name>]
                                [-u <uuid>]
                                [-p <project>]
                                [--note <note>]

**Optional arguments:**

.. option:: -n <name>, --name <name>

    Name of the region.

.. option:: -u <uuid>, --uuid <uuid>

    UUID of the region.

.. option:: -p <project>, --project <project>, --project_uuid <project>

    UUID of the project that this region belongs to.

.. option:: --note <note>

    Note about the region.


craton region-delete
--------------------

.. program:: craton region-delete

Delete a region.

::

    usage: craton region-delete <region>

**Positional arguments:**

.. option:: region

    UUID of the region.

craton region-list
------------------

.. program:: craton region-list

List the regions.

::

    usage: craton region-list [--detail] [--limit <limit>]
                              [--sort-key <field>] [--sort-dir <direction>]
                              [--fields <field> [<field> ...]]

**Optional arguments:**

.. option:: --detail

    Show detailed information about the regions.

.. option:: --limit <limit>

    Maximum number of regions to return per request, 0 for no limit. Default
    is the maximum number used by the Craton API Service.

.. option:: --sort-key <field>

    Region field that will be used for sorting.

.. option:: --sort-dir <direction>

    Sort direction: “asc” (the default) or “desc”.

.. option:: --fields <field> [<field> ...]

    One or more region fields. Only these fields will be fetched from the
    server.  Can not be used when ‘-- detail’ is specified.

craton region-show
------------------

.. program:: craton region-show

Show detailed information about a region.

::

    usage: craton region-show <region>

**Positional arguments:**

.. option:: region

    UUID of the region.

craton region-update
--------------------

.. program:: craton region-update

Update information about a region.

::

    usage: craton region-update <region> [-n <name>]

**Positional arguments:**

.. option:: region

    UUID of the region.

**Optional arguments:**

.. option:: -n <name>, --name <name>

    New name for the region.


craton cell-create
------------------

.. program:: craton cell-create

Create a new cell.

::

    usage: craton cell-create [-n <name>]
                            [-u <uuid>]
                            [-p <project>]
                            [-r <region>]
                            [--note <note>]

**Optional arguments:**

.. option:: -n <name>, --name <name>

    Name of the cell.

.. option:: -u <uuid>, --uuid <uuid>

    UUID of the cell.

.. option:: -p <project>, --project <project>, --project_uuid <project>

    UUID of the project that this cell belongs to.

.. option:: -r <region>, --region <region>, --region_uuid <region>

    UUID of the region that this cell belongs to.

.. option:: --note <note>

    Note about the cell.


craton cell-delete
------------------

.. program:: craton cell-delete

Delete a cell.

::

    usage: craton cell-delete <cell>

**Positional arguments:**

.. option:: cell

    UUID of the cell.


craton cell-list
----------------

.. program:: craton cell-list

List the cells.

::

    usage: craton cell-list [--detail] [--limit <limit>]
                            [--sort-key <field>] [--sort-dir <direction>]
                            [--fields <field> [<field> ...]]
                            [--region <region>]

**Optional arguments:**

.. option:: --detail

    Show detailed information about the cells.

.. option:: -r <region>, --region <region>

    UUID of the region that contains the desired list of cells.

.. option:: --limit <limit>

    Maximum number of cells to return per request, 0 for no limit. Default is
    the maximum number used by the Craton API Service.

.. option:: --sort-key <field>

    Cell field that will be used for sorting.

.. option:: --sort-dir <direction>

    Sort direction: “asc” (the default) or “desc”.

.. option:: --fields <field> [<field> ...]

    One or more cell fields. Only these fields will be fetched from the
    server.  Can not be used when ‘-- detail’ is specified.


craton cell-show
----------------

.. program:: craton cell-show

Show detailed information about a cell.

::

    usage: craton cell-show <cell>

**Positional arguments:**

.. option:: cell

    UUID of the cell.


craton cell-update
------------------

.. program:: craton cell-update

Update information about a cell.

::

    usage: craton cell-update <cell> [-n <name>]

**Positional arguments:**

.. option:: cell

    UUID of the cell.

**Optional arguments:**

.. option:: -n <name>, --name <name>

    New name for the cell.


craton device-create
--------------------

.. program:: craton device-create

Create a new device.

::

    usage: craton device-create [-n <name>]
                            [-t <type>]
                            [-a <active>]
                            [-u <uuid>]
                            [-p <project>]
                            [-r <region>]
                            [-c <cell>]
                            [--note <note>]

**Optional arguments:**

.. option:: -n <name>, --name <name>

    Name of the device.

.. option:: -t <type>, --type <type>

    Type of device.

.. option:: -a <active>, --active <active>

    Active or inactive state for a device: ‘true’ or ‘false’.

.. option:: -u <uuid>, --uuid <uuid>

    UUID of the device.

.. option:: -p <project>, --project <project>, --project_uuid <project>

    UUID of the project that this device belongs to.

.. option:: -r <region>, --region <region>, --region_uuid <region>

    UUID of the region that this device belongs to.

.. option:: -c <cell>, --cell <cell>, --cell_uuid <cell>

    UUID of the cell that this device belongs to.

.. option:: --note <note>

    Note about the device.


craton device-delete
--------------------

.. program:: craton device-delete

Delete a device.

::

    usage: craton device-delete <device>

**Positional arguments:**

.. option:: device

    UUID of the device.


craton device-list
------------------

.. program:: craton device-list

List the devices.

::

    usage: craton device-list [--detail] [--limit <limit>]
                              [--sort-key <field>] [--sort-dir <direction>]
                              [--fields <field> [<field> ...]]
                              [--cell <cell>]

**Optional arguments:**

.. option:: -c <cell>, --cell <cell>

    UUID of the cell that contains the desired list of devices.

.. option:: --detail

    Show detailed information about the device.

.. option:: --limit <limit>

    Maximum number of devices to return per request, 0 for no limit. Default
    is the maximum number used by the Craton API Service.

.. option:: --sort-key <field>

    Device field that will be used for sorting.

.. option:: --sort-dir <direction>

    Sort direction: “asc” (the default) or “desc”.

.. option:: --fields <field> [<field> ...]

    One or more device fields. Only these fields will be fetched from the
    server.  Can not be used when ‘-- detail’ is specified.


craton device-show
------------------

.. program:: craton device-show

Show detailed information about a device.

::

    usage: craton device-show <device>

**Positional arguments:**

.. option:: device

    UUID of the device.


craton device-update
--------------------

.. program:: craton device-update

Update information about a device.

::

    usage: craton device-update <device> [-n <name>]

**Positional arguments:**

.. option:: device

    UUID of the device.

**Optional arguments:**

.. option:: -n <name>, --name <name>

    New name for the device.


craton host-create
------------------

.. program:: craton host-create

Create a new host.

::

    usage: craton host-create [-n <name>]
                            [-t <type>]
                            [-a <active>]
                            [-u <uuid>]
                            [-p <project>]
                            [-r <region>]
                            [-c <cell>]
                            [--note <note>]
                            [--access_secret <access_secret>]
                            [-i <ip_address>]

**Optional arguments:**

.. option:: -n <name>, --name <name>

    Name of the host.

.. option:: -t <type>, --type <type>

    Type of host.

.. option:: -a <active>, --active <active>

    Active or inactive state for a host: ‘true’ or ‘false’.

.. option:: -u <uuid>, --uuid <uuid>

    UUID of the host.

.. option:: -p <project>, --project <project>, --project_uuid <project>

    UUID of the project that this host belongs to.

.. option:: -r <region>, --region <region>, --region_uuid <region>

    UUID of the region that this host belongs to.

.. option:: -c <cell>, --cell <cell>, --cell_uuid <cell>

    UUID of the cell that this host belongs to.

.. option:: --note <note>

    Note about the host.

.. option:: --access_secret <access_secret>

    UUID of the access secret of the host.

.. option:: -i <ip_address>, --ip_address <ip_address>

    IP Address type of the host.


craton host-delete
------------------

.. program:: craton host-delete

Delete a host.

::

    usage: craton host-delete <host>

**Positional arguments:**

.. option:: host

    UUID of the host.


craton host-list
----------------

.. program:: craton host-list

List the hosts.

::

    usage: craton host-list [--detail] [--limit <limit>]
                         [--sort-key <field>] [--sort-dir <direction>]
                         [--fields <field> [<field> ...]]
                         [--cell <cell>]

**Optional arguments:**

.. option:: -c <cell>, --cell <cell>

    UUID of the cell that contains the desired list of hosts.

.. option:: --detail

    Show detailed information about the host.

.. option:: --limit <limit>

    Maximum number of hosts to return per request, 0 for no limit. Default is
    the maximum number used by the Craton API Service.

.. option:: --sort-key <field>

    Host field that will be used for sorting.

.. option:: --sort-dir <direction>

    Sort direction: “asc” (the default) or “desc”.

.. option:: --fields <field> [<field> ...]

    One or more host fields. Only these fields will be fetched from the
    server.  Can not be used when ‘-- detail’ is specified.


craton host-show
----------------

.. program:: craton host-show

Show detailed information about a host.

::

    usage: craton host-show <host>

**Positional arguments:**

.. option:: host

    UUID of the host.


craton host-update
------------------

.. program:: craton host-update

Update information about a host.

::

    usage: craton host-update <host> [-n <name>]

**Positional arguments:**

.. option:: host

    UUID of the host.

**Optional arguments:**

.. option:: -n <name>, --name <name>

    New name for the host.


craton user-list
----------------

.. program:: craton user-list

List the users in a project.

::

    usage: craton user-list [--detail] [--limit <limit>]
                         [--sort-key <field>] [--sort-dir <direction>]
                         [--fields <field> [<field> ...]]

**Optional arguments:**

.. option:: --detail

    Show detailed information about the users.

.. option:: --limit <limit>

    Maximum number of users to return per request, 0 for no limit. Default is
    the maximum number used by the Craton API Service.

.. option:: --sort-key <field>

    User field that will be used for sorting.

.. option:: --sort-dir <direction>

    Sort direction: “asc” (the default) or “desc”.

.. option:: --fields <field> [<field> ...]

    One or more user fields. Only these fields will be fetched from the
    server.  Can not be used when ‘-- detail’ is specified.
