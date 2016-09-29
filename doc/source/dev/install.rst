
=====================================================
Installing and Setting up a Development Environment
=====================================================

Installation
============

--------------------------------------------
Installing Environment from packages: Ubuntu
--------------------------------------------


* Install a fresh Ubuntu image

* Make sure we have git installed::

    # apt-get update
    # apt-get install git -y

* Clone the repository::

    # git clone https://github.com/openstack/craton.git

* Install the prerequisite packages::

    # sudo apt-get install python-dev
    # sudo apt-get install python-pip
    # sudo apt-get install python-setuptools
    # sudo pip install --upgrade pip
    # sudo pip install --upgrade setuptools

* Goto craton directory and install the following::

    # sudo pip install -r requirements.txt
    # sudo python setup.py install

* Install mariadb and make sure mysql is running::

    # sudo apt-get install mariadb-server
    # sudo service mysql start

* Ensure you have python-mysqldb installed::

    # sudo apt-get install python-mysqldb

--------------------------------------------------------
Installing Environment from packages: Fedora/CentOS etc. 
--------------------------------------------------------


* Install a fresh Fedora/CentOS image

* Make sure we have git installed::

    # yum update
    # yum install git -y

* Clone the repository::

    # git clone https://github.com/openstack/craton.git

* Install the prerequisite packages::

    # sudo yum install python-devel
    # sudo yum install python-pip
    # sudo yum install python-setuptools
    # sudo pip install --upgrade pip
    # sudo pip install --upgrade setuptools

* Goto craton directory and install the following::

    # sudo pip install -r requirements.txt
    # sudo python setup.py install

* Install mariadb and make sure mysql is running::

    # sudo yum install mariadb-server
    # sudo service mysql start

* Ensure you have python-mysqldb installed::

    # sudo yum install MySQL-python

--------------
Database Setup
--------------

* Connect to database server as root user::

    # mysql -u root -p

* Create user craton::

    # CREATE USER 'craton'@'localhost' IDENTIFIED BY 'craton';

* Grant proper access to the craton user and flush privileges::

    # GRANT ALL PRIVILEGES ON craton.* TO 'craton'@'localhost'
    identified by 'craton';
    # FLUSH PRIVILEGES;

* You can verify that the user was added by calling::

    # select host, user, password from mysql.user;

* Create the Craton database::

    # create database craton;

* Logout from the database server::

    # exit

------------------------------------
Modify etc/inventory-api-conf.sample
------------------------------------

* Make api_paste_config use a fully qualified path (not relative).
  This will be specific for your machine

.. Note:: Make sure you have the proper path for inventory-api-conf.sample

    # api_paste_config=/home/cratonuser/craton/etc/inventory-api-paste.ini

* Add the following line to the [database] section:

    # connection = mysql://craton:craton@localhost/craton

* Update the host in the [api] section to match your IP:

    # host = xxx.xxx.xxx.xxx

----------
Run dbsync
----------

* Make sure to run dbsync to get the db tables created::

    # craton-inventory-dbsync --config-file=etc/inventory
    -api-conf.sample version
    # craton-inventory-dbsync --config-file=etc/inventory
    -api-conf.sample upgrade

-----------------------
Create Project and User
-----------------------

.. Note:: These goes away once the API has been setup

* Connect to database server as root user::

    # mysql -u root -p

* Use the database craton::

    # use craton;

* Modify the projects and users as following::

    # insert into projects (created_at, updated_at, name) values
    (NOW(), NOW(), "osic");
    # insert into users (created_at, updated_at, project_id, username
    , api_key, is_admin)
    values (NOW(), NOW(), 1, "demo", "demo", False);

* Logout from the database server::

    # exit

---------------------
Start the API Service
---------------------

* To start the API service, run the following command::

    # python craton/cmd/inventory-api.py --config-file=etc/
    inventory-api-conf.sample


* Some examples of API calls are as below:

---------------
Create a Region
---------------

* In order to create the region, export the IP address you set in
  /etc/inventory-api-conf.sample::

    # export MY_IP=xxx.xxx.xxx.xxx

* To create region, execute the following command::

    # curl -i "http://${MY_IP}:8080/v1/regions" -XPOST -d
    '{"name": "DFW", "project_id": 1}' -H "Content-Type: application/json"
    -H "X-Auth-Token: demo" -H "X-Auth-User: demo" -H "X-Auth-Project: 1"

------------------
Get created Region
------------------

* To get the created region, execute the following command::

    # curl -i "http://${MY_IP}:8080/v1/regions" -H "Content-Type:
    application/json" -H "X-Auth-Token: demo" -H "X-Auth-User:
    demo" -H "X-Auth-Project: 1"

--------------------------
Get all hosts for Region 1
--------------------------

* To get all hosts for region 1, execute the following command::

    # curl -i "http://${MY_IP}:8080/v1/hosts?region_id=1"
    -H "Content-Type: application/json" -H "X-Auth-Token: demo"
    -H "X-Auth-User: demo" -H "X-Auth-Project: 1"

---------------------
Get a particular host
---------------------

* To get a particular host, execute the following command::

    # curl -i "http://${MY_IP}:8080/v1/hosts/33" -H
    "Content-Type: application/json" -H "X-Auth-Token: demo"
    -H "X-Auth-User: demo" -H "X-Auth-Project: 1"
