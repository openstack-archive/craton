#!/bin/sh

# This script will execute before OpenStack infrastructure revokes sudo
# We need it to allow the Jenkins user to interact with docker

# This tells docker to use the current user's primary group to run the unix
# domain socket for docker. This side-steps the need for the current user to
# be added to the docker group and then have to log out and back in.
#sudo mkdir -p /etc/default
#echo "DOCKER_OPTS=\"-D --group=$(id -gn)\"" | sudo tee /etc/default/docker
sudo dd of=/lib/systemd/system/docker.socket << _EOF_
[Unit]
Description=Docker Socket for the API
PartOf=docker.service

[Socket]
ListenStream=/var/run/docker.sock
SocketMode=0660
SocketUser=root
SocketGroup=$(id -gn)

[Install]
WantedBy=sockets.target
_EOF_

echo "=> Restarting docker"
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Checking permissions on the socket"
stat /var/run/docker.sock

echo "=> Discovering docker version installed"
docker version
