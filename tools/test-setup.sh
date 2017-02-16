#!/bin/sh

# This script will execute before OpenStack infrastructure revokes sudo
# We need it to allow the Jenkins user to interact with docker

# This tells docker to use the current user's primary group to run the unix
# domain socket for docker. This side-steps the need for the current user to
# be added to the docker group and then have to log out and back in.
sudo mkdir -p /etc/default
echo "DOCKER_OPTS=\"--group=$(id -gn)\"" | sudo tee /etc/default/docker
echo "=> Restarting docker"
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "=> Discovering docker version installed"
docker version
