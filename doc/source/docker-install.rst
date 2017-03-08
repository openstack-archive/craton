
=======================
Installing using Docker
=======================

Installation
============

-------------------------------------
Installing necessary packages: Ubuntu
-------------------------------------


* Make sure git is installed::

    $ sudo apt-get update
    $ sudo apt-get install git -y

* Clone the Craton repository::

    $ git clone https://github.com/openstack/craton.git

* To install Docker, follow the instructions found here:
    https://docs.docker.com/engine/installation/linux/ubuntulinux/


-------------------------------------------------
Installing necessary packages: Fedora/CentOS etc.
-------------------------------------------------


* Install a fresh Fedora/CentOS image

* Make sure we have git installed::

    $ sudo yum update
    $ sudo yum install git -y

* Clone the repository::

    $ git clone https://github.com/openstack/craton.git

* Follow the correct Docker install guide for your operating system::

    Fedora: https://docs.docker.com/engine/installation/linux/fedora/
    CentOS: https://docs.docker.com/engine/installation/linux/centos/


---------------------------
Run the Craton Docker Image
---------------------------

* First, go to craton directory and build the Docker image::

    $ sudo docker build --pull -t craton-api:latest .

* And finally, run the docker image::

    $ sudo docker run -t --name craton-api -d craton-api:latest


-------------------
Calling into Craton
-------------------

* Let's get container Id::

    $ ContainerId=$(docker ps | grep craton-api:latest | awk '{print $1}')

* We need the container IP, so we can run an API call against Craton running in the container::

    $ ContainerIP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${ContainerId})

* To generate a sample data set, use the following command::

    $ python tools/generate_fake_data.py --url http://${ContainerIP}:8080/v1 --user demo --project b9f10eca66ac4c279c139d01e65f96b4 --key demo

* Now you can run a curl command like the one below to query Craton::

    $ curl -i "http://${ContainerIP}:8080/v1/hosts?region_id=1" -H "Content-Type: application/json" -H "X-Auth-Token: demo" -H "X-Auth-User: demo" -H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4"


-------------------
Command Cheat-Sheet
-------------------

* Get the Craton logs::

    $ docker logs -f craton-api

* Open mysql in the Craton container::

    $ docker exec -it craton-api mysql -ucraton -pcraton craton

* Get a bash shell from the Craton container::

    $ docker exec -it craton-api bash # for a bash shell, etc



