#!/bin/sh

# This script will execute before OpenStack infrastructure revokes sudo
# We need it to allow the Jenkins user to interact with docker

echo "=> Add user to docker group"
sudo gpasswd -a ${USER} docker
echo "=> Restarting docker"
sudo systemctl daemon-reload
sudo systemctl restart docker
echo "=> User permissions: $(id)"
echo "=> Discovering docker version installed"
docker version
