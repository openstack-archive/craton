#!/bin/sh

# This script will execute before OpenStack infrastructure revokes sudo
# We need it to allow the Jenkins user to interact with docker

sudo gpasswd -a ${USER} docker
sudo systemctl daemon-reload
sudo systemctl restart docker
docker version
