=========
Inventory
=========

Using Ansible inventory requirements as motivations, defines hosts,
host variables, groups, secrets, references to group variables,
tenants, regions; and corresponding queries.

A SQLAlchemy-based ORM backend is provided, but it is also possible
(with a suitable implementation) to plug in alternative
backends. Usually this would be to use such a backend based on a REST
API, such as against an existing asset database.

