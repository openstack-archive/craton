..

==================================
Craton service command-line client
==================================


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

**craton usage**
    Show usages of craton client.
**craton project-create**
    Create a new project.
**craton project-delete**
    Delete a project.
**craton project-list**
    List all projects.
**craton project-show**
    Show detailed information about a project.
**craton project-update**
    Update information about a project.
**craton region-create**
    Create a new region.
**craton region-delete**
    Delete a region.
**craton region-list**
    List all regions.
**craton region-show**
    Show detailed information about a region.
**craton region-update**
    Update information about a region.
**craton cell-create**
    Create a new cell.
**craton cell-delete**
    Delete a cell.
**craton cell-list**
    List all cells.
**craton cell-show**
    Show detailed information about a cell.
**craton cell-update**
    Update information about a cell.
**craton device-create**
    Create a new device.
**craton device-delete**
    Delete a device.
**craton device-list**
    List all devices.
**craton device-show**
    Show detailed information about a device.
**craton device-update**
    Update information about a device.
**craton host-create**
    Create a new host.
**craton host-delete**
    Delete a host.
**craton host-list**
    List all hosts.
**craton host-show**
    Show detailed information about a host.
**craton host-update**
    Update information about a host.
**craton user-list**
    List the users of a project.
**craton help**
    Display help about this program or one of its subcommands.

craton optional arguments
-------------------------

``--version``
 Show program's version number and exits.
``-v, --verbose``
 Print more verbose output.

craton project-create
---------------------
Create a new project.
::

 usage: craton project-create [-n <name>] [-u <uuid>]

**Optional arguments:**

``-n <name>, --name <name>``
 Name of the project.

``-u <uuid>, --uuid <uuid>``
 UUID of the project.


craton project-delete
---------------------
Delete a project.
::

 usage: craton project-delete <project>

**Positional arguments:**

``<project>``
 UUID of the project.

craton project-list
-------------------
List the projects.
::

 usage: craton project-list [--detail] [--limit <limit>]

**Optional arguments:**

``--detail``
 Show detailed information about the projects.
``--limit <limit>``
 Maximum number of projects to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

craton project-show
-------------------
Show detailed information about a project.
::

 usage: craton project-show <project>

**Positional arguments:**

``<project>``
 UUID of the project.


craton project-update
---------------------
Update information about a project.
::

 usage: craton project-update <project> [-n <name>]

**Positional arguments:**

``<project>``
 UUID of the project.

**Optional arguments:**

``-n <name>, --name <name>``
 New name for the project.

craton region-create
--------------------
Create a new region.
::

 usage: craton region-create [-n <name>] [-u <uuid>] [-p <project>] [--note <note>]

**Optional arguments:**

``-n <name>, --name <name>``
 Name of the region.

``-u <uuid>, --uuid <uuid>``
 UUID of the region.

``-p <project>, --project <project>, --project_uuid <project>``
 UUID of the project that this region belongs to.

``--note <note>``
 Note about the region.

craton region-delete
--------------------
Delete a region.
::

 usage: craton region-delete <region>

**Positional arguments:**

``<region>``
 UUID of the region.

craton region-list
------------------
List the regions.
::

 usage: craton region-list [--detail] [--limit <limit>]
                           [--sort-key <field>] [--sort-dir <direction>]
                           [--fields <field> [<field> ...]]

**Optional arguments:**

``--detail``
 Show detailed information about the regions.

``--limit <limit>``
 Maximum number of regions to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

``--sort-key <field>``
 Region field that will be used for sorting.

``--sort-dir <direction>``
 Sort direction: “asc” (the default) or “desc”.

``--fields <field> [<field> ...]``
 One or more region fields. Only these fields will be fetched from the server. Can not be used when ‘-- detail’ is specified.

craton region-show
------------------
Show detailed information about a region.
::

 usage: craton region-show <region>

**Positional arguments:**

``<region>``
 UUID of the region.

craton region-update
--------------------
Update information about a region.
::

 usage: craton region-update <region> [-n <name>]

**Positional arguments:**

``<region>``
 UUID of the region.

**Optional arguments:**

``-n <name>, --name <name>``
 New name for the region.

craton cell-create
------------------
Create a new cell.
::

 usage: craton cell-create [-n <name>] [-u <uuid>] [-p <project>] [-r <region>] [--note <note>]

**Optional arguments:**

``-n <name>, --name <name>``
 Name of the cell.

``-u <uuid>, --uuid <uuid>``
 UUID of the cell.

``-p <project>, --project <project>, --project_uuid <project>``
 UUID of the project that this cell belongs to.

``-r <region>, --region <region>, --region_uuid <region>``
 UUID of the region that this cell belongs to.

``--note <note>``
 Note about the cell.

craton cell-delete
------------------
Delete a cell.
::

 usage: craton cell-delete <cell>

**Positional arguments:**

``<cell>``
 UUID of the cell.

craton cell-list
----------------
List the cells.
::

 usage: craton cell-list [--detail] [--limit <limit>]
                         [--sort-key <field>] [--sort-dir <direction>]
                         [--fields <field> [<field> ...]]
                         [--region <region>]

**Optional arguments:**

``--detail``
 Show detailed information about the cells.

``-r <region>, --region <region>``
 UUID of the region that contains the desired list of cells.

``--limit <limit>``
 Maximum number of cells to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

``--sort-key <field>``
 Cell field that will be used for sorting.

``--sort-dir <direction>``
 Sort direction: “asc” (the default) or “desc”.

``--fields <field> [<field> ...]``
 One or more cell fields. Only these fields will be fetched from the server. Can not be used when ‘-- detail’ is specified.

craton cell-show
----------------
Show detailed information about a cell.
::

 usage: craton cell-show <cell>

**Positional arguments:**

``<cell>``
 UUID of the cell.

craton cell-update
------------------
Update information about a cell.
::

 usage: craton cell-update <cell> [-n <name>]

**Positional arguments:**

``<cell>``
 UUID of the cell.

**Optional arguments:**

``-n <name>, --name <name>``
 New name for the cell.

craton device-create
--------------------
Create a new device.
::

 usage: craton device-create [-n <name>] [-t <type>] [-a <active>] [-u <uuid>] [-p <project>] [-r <region>] [-c <cell>] [--note <note>]

**Optional arguments:**

``-n <name>, --name <name>``
 Name of the device.

``-t <type>, --type <type>``
 Type of device.

``-a <active>, --active <active>``
 Active or inactive state for a device: ‘true’ or ‘false’.

``-u <uuid>, --uuid <uuid>``
 UUID of the device.

``-p <project>, --project <project>, --project_uuid <project>``
 UUID of the project that this device belongs to.

``-r <region>, --region <region>, --region_uuid <region>``
 UUID of the region that this device belongs to.

``-c <cell>, --cell <cell>, --cell_uuid <cell>``
 UUID of the cell that this device belongs to.

``--note <note>``
 Note about the device.

craton device-delete
--------------------
Delete a device.
::

 usage: craton device-delete <device>

**Positional arguments:**

``<device>``
 UUID of the device.

craton device-list
------------------
List the devices.
::

 usage: craton device-list [--detail] [--limit <limit>]
                           [--sort-key <field>] [--sort-dir <direction>]
                           [--fields <field> [<field> ...]]
                           [--cell <cell>]

**Optional arguments:**

``-c <cell>, --cell <cell>``
 UUID of the cell that contains the desired list of devices.

``--detail``
 Show detailed information about the device.

``--limit <limit>``
 Maximum number of devices to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

``--sort-key <field>``
 Device field that will be used for sorting.

``--sort-dir <direction>``
 Sort direction: “asc” (the default) or “desc”.

``--fields <field> [<field> ...]``
 One or more device fields. Only these fields will be fetched from the server. Can not be used when ‘-- detail’ is specified.

craton device-show
------------------
Show detailed information about a device.
::

 usage: craton device-show <device>

**Positional arguments:**

``<device>``
 UUID of the device.

craton device-update
--------------------
Update information about a device.
::

 usage: craton device-update <device> [-n <name>]

**Positional arguments:**

``<device>``
 UUID of the device.

**Optional arguments:**

``-n <name>, --name <name>``
 New name for the device.

craton host-create
------------------
Create a new host.
::

 usage: craton host-create [-n <name>] [-t <type>] [-a <active>] [-u <uuid>] [-p <project>] [-r <region>] [-c <cell>] [--note <note>] [--access_secret <access_secret>] [-i <ip_address>]

**Optional arguments:**

``-n <name>, --name <name>``
 Name of the host.

``-t <type>, --type <type>``
 Type of host.

``-a <active>, --active <active>``
 Active or inactive state for a host: ‘true’ or ‘false’.

``-u <uuid>, --uuid <uuid>``
 UUID of the host.

``-p <project>, --project <project>, --project_uuid <project>``
 UUID of the project that this host belongs to.

``-r <region>, --region <region>, --region_uuid <region>``
 UUID of the region that this host belongs to.

``-c <cell>, --cell <cell>, --cell_uuid <cell>``
 UUID of the cell that this host belongs to.

``--note <note>``
 Note about the host.

``--access_secret <access_secret>``
 UUID of the access secret of the host.

``-i <ip_address>, --ip_address <ip_address>``
 IP Address type of the host.

craton host-delete
------------------
Delete a host.
::

 usage: craton host-delete <host>

**Positional arguments:**

``<host>``
 UUID of the host.

craton host-list
----------------
List the hosts.
::

 usage: craton host-list [--detail] [--limit <limit>]
                         [--sort-key <field>] [--sort-dir <direction>]
                         [--fields <field> [<field> ...]]
                         [--cell <cell>]

**Optional arguments:**

``-c <cell>, --cell <cell>``
 UUID of the cell that contains the desired list of hosts.

``--detail``
 Show detailed information about the host.

``--limit <limit>``
 Maximum number of hosts to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

``--sort-key <field>``
 Host field that will be used for sorting.

``--sort-dir <direction>``
 Sort direction: “asc” (the default) or “desc”.

``--fields <field> [<field> ...]``
 One or more host fields. Only these fields will be fetched from the server. Can not be used when ‘-- detail’ is specified.

craton host-show
----------------
Show detailed information about a host.
::

 usage: craton host-show <host>

**Positional arguments:**

``<host>``
 UUID of the host.

craton host-update
------------------
Update information about a host.
::

 usage: craton host-update <host> [-n <name>]

**Positional arguments:**

``<host>``
 UUID of the host.

**Optional arguments:**

``-n <name>, --name <name>``
 New name for the host.


craton user-list
------------------------
List the users in a project.
::

 usage: craton user-list [--detail] [--limit <limit>]
                         [--sort-key <field>] [--sort-dir <direction>]
                         [--fields <field> [<field> ...]]

**Optional arguments:**

``--detail``
 Show detailed information about the users.

``--limit <limit>``
 Maximum number of users to return per request, 0 for no limit. Default is the maximum number used by the Craton API Service.

``--sort-key <field>``
 User field that will be used for sorting.

``--sort-dir <direction>``
 Sort direction: “asc” (the default) or “desc”.

``--fields <field> [<field> ...]``
 One or more user fields. Only these fields will be fetched from the server. Can not be used when ‘-- detail’ is specified.