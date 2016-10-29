
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

    S sudo docker build -t craton-api:latest .

* And finally, run the docker image::

    $ sudo docker run -t --name craton-api -p 127.0.0.1:8080:8080 -d craton-api:latest


-------------------
Calling into Craton
-------------------

* To generate a sample data set, use the following command::

    $ python tools/generate_fake_data.py --url http://127.0.0.1:8080/v1 --user demo --project b9f10eca66ac4c279c139d01e65f96b4 --key demo

* Now, let's run an API call against Craton running in the container. First, we need to enumerate the running Docker images::

    $ sudo docker ps

* Use the container id from that command in this next command to find the container's IP address::

    $ sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${ContainerId}

* Now that you know the IP address, you can run a curl command like the one below to query Craton::

    $ curl -i "http://172.17.0.11:8080/v1/hosts?region_id=1" -H "Content-Type: application/json" -H "X-Auth-Token: demo" -H "X-Auth-User: demo" -H "X-Auth-Project: 1"



-------------------
Command Cheat-Sheet
-------------------

* Get the Craton logs::

    $ docker logs -f craton-api

* Open mysql in the Craton container::

    $ docker exec -it craton-api mysql -ucraton -pcraton craton

* Get a bash shell from the Craton container::

    $ docker exec -it craton-api bash # for a bash shell, etc



