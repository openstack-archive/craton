
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

.. note:: This is a Python3 project only, the minimum support version is Python 3.5.

* Install the prerequisite packages::

    # sudo apt-get install python3.5 python3.5-dev
    # sudo apt-get install python3-pip python3-setuptools
    # sudo pip3 install --upgrade pip
    # sudo pip3 install --upgrade setuptools

* Goto craton directory and install the following::

    # sudo pip3 install -r requirements.txt
    # sudo python3 setup.py install

* Install mariadb and make sure mysql is running::

    # sudo apt-get install mariadb-server
    # sudo service mysql start

* Ensure you have python3-mysqldb installed::

    # sudo apt-get install python3-mysqldb

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

    # sudo yum install python3-devel
    # sudo yum install python3-pip
    # sudo yum install python3-setuptools
    # sudo pip3 install --upgrade pip
    # sudo pip3 install --upgrade setuptools

* Goto craton directory and install the following::

    # sudo pip3 install -r requirements.txt
    # sudo python3 setup.py install

* Install mariadb and make sure mysql is running::

    # sudo yum install mariadb-server
    # sudo service mysql start

* Ensure you have python3-mysql installed::

    # sudo yum install python3-mysql

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

    # create database craton CHARACTER SET='utf8';

* Logout from the database server::

    # exit

------------------------------------
Modify etc/craton-api-conf.sample
------------------------------------

* Make api_paste_config use a fully qualified path (not relative).
  This will be specific for your machine

.. note:: Make sure you have the proper path for craton-api-conf.sample

    # api_paste_config=/home/cratonuser/craton/etc/craton-api-paste.ini

* Add the following line to the [database] section:

    # connection = mysql://craton:craton@localhost/craton

* Update the host in the [api] section to match your IP:

    # host = xxx.xxx.xxx.xxx

----------
Run dbsync
----------

* Make sure to run dbsync to get the db tables created::

    # craton-dbsync --config-file=etc/craton
    -api-conf.sample version
    # craton-dbsync --config-file=etc/craton
    -api-conf.sample upgrade

-----------------------
Create Project and User
-----------------------

.. note:: These goes away once the API has been setup

* Connect to database server as root user::

    # mysql -u root -p

* Use the database craton::

    # use craton;

* Modify the projects and users as following::

    # insert into projects (created_at, updated_at, name, id) values
    (NOW(), NOW(), "osic", "717e9a216e2d44e0bc848398563bda06");
    # insert into users (created_at, updated_at, project_id, username
    , api_key, is_admin)
    values (NOW(), NOW(), "717e9a216e2d44e0bc848398563bda06", "demo", "demo", False);

* Logout from the database server::

    # exit

---------------------
Start the API Service
---------------------

* To start the API service, run the following command::

    # craton-api --config-file=etc/
    craton-api-conf.sample


* Some examples of API calls are as below:

---------------
Create a Region
---------------

* In order to create the region, export the IP address you set in
  /etc/craton-api-conf.sample::

    # export MY_IP=xxx.xxx.xxx.xxx

* Next create a cloud to which the region is associated to::

    # curl -i "http://${MY_IP}:7780/v1/clouds" \
           -d '{"name": "Cloud_Sample"}' \
           -H "Content-Type: application/json" \
           -H "X-Auth-Token: demo" \
           -H "X-Auth-User: demo" \
           -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

* To create region, execute the following command::

    # curl -i "http://${MY_IP}:7780/v1/regions" \
           -d '{"name": "DFW", "project_id": "717e9a216e2d44e0bc848398563bda06", "cloud_id": 1}' \
           -H "Content-Type: application/json" \
           -H "X-Auth-Token: demo" \
           -H "X-Auth-User: demo" \
           -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

------------------
Get created Region
------------------

* To get the created region, execute the following command::

    # curl -i "http://${MY_IP}:7780/v1/regions" \
           -H "Content-Type: application/json" \
           -H "X-Auth-Token: demo" \
           -H "X-Auth-User: demo" \
           -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

--------------------------
Get all hosts for Region 1
--------------------------

* To get all hosts for region 1, execute the following command::

    # curl -i "http://${MY_IP}:7780/v1/hosts?region_id=1" \
           -H "Content-Type: application/json" \
           -H "X-Auth-Token: demo" \
           -H "X-Auth-User: demo" \
           -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

---------------------
Get a particular host
---------------------

* To get a particular host, execute the following command::

    # curl -i "http://${MY_IP}:7780/v1/hosts/33" \
           -H "Content-Type: application/json" \
           -H "X-Auth-Token: demo" \
           -H "X-Auth-User: demo" \
           -H "X-Auth-Project: 717e9a216e2d44e0bc848398563bda06"

-------------
Running Tests
-------------

* To run unit tests, execute the following command::

    # tox

* To run functional tests, execute the following command::

    # tox -e functional
