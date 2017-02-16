#!/bin/sh

# This script will execute before OpenStack infrastructure revokes sudo
# We need it to allow the Jenkins user to interact with docker

sudo groupadd docker
sudo gpasswd -a jenkins docker
sudo service docker restart
docker version
