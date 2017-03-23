
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

* Bootstrap credentials are generated at the top of the craton-api logs for initial authentication. You can manually copy the username, api key, and project id from the logs by running::

    $ docker logs -f craton-api

  Or you can grep for them::

    $ CRATON_PROJECT_ID=$(docker logs craton-api | grep "ProjectId:" | awk '{print $2}' | tr -d '\r')
    $ CRATON_USERNAME=$(docker logs craton-api | grep "Username:" | awk '{print $2}' | tr -d '\r')
    $ CRATON_API_KEY=$(docker logs craton-api | grep "APIKey:" | awk '{print $2}' | tr -d '\r')

* To generate a sample data set, use the following command::

    $ python tools/generate_fake_data.py --url http://${ContainerIP}:7780/v1 --user "$CRATON_USERNAME" --project "$CRATON_PROJECT_ID" --key "$CRATON_API_KEY"

* Now you can run a curl command like the one below to query Craton::

    $ curl -i "http://${ContainerIP}:7780/v1/hosts?region_id=1" -H "Content-Type: application/json" -H "X-Auth-Token: ${CRATON_API_KEY}" -H "X-Auth-User: ${CRATON_USERNAME}" -H "X-Auth-Project: ${CRATON_PROJECT_ID}"

-----------------------
Using wrapper functions
-----------------------

*Some wrapper functions have been included in craton/tools to quickly build, reload, populate, and query craton.
* To load the wrapper functions, run the following in the craton parent directory::

    # source tools/wrapper-functions.sh

* To quick start and populate craton in docker, run the following from the craton parent directory::

    # craton-docker-start

* In order to interact with craton, export the bootstrap credentials by running::

    # eval $(craton-docker-env)

* Populate craton with fake data by running::

    # craton-fake-data

* Run API calls against craton with the following wrappers::
.. note:: *Requires the installation of httpie*

    # craton-post v1/regions name=HKG
    # craton-get v1/hosts
    # craton-put v1/hosts/3 device_type=container
    # craton-put v1/hosts/3/variables foo=47 bar:='["a", "b", "c"]'
    # craton-delete v1/hosts/4

-------------------
Command Cheat-Sheet
-------------------

* Get the Craton logs::

    $ docker logs -f craton-api

* Open mysql in the Craton container::

    $ docker exec -it craton-api mysql -ucraton -pcraton craton

* Get a bash shell from the Craton container::

    $ docker exec -it craton-api bash # for a bash shell, etc
