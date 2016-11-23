#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

############################################################################
# Usage:
# docker build --pull -t craton-api:latest .
# docker run -t --name craton-api -p 127.0.0.1:8080:8080 -d craton-api:latest
# python tools/generate_fake_data.py --url http://127.0.0.1:8080/v1 --user demo --project b9f10eca66ac4c279c139d01e65f96b4 --key demo
# curl http://127.0.0.1:8080/v1/regions -H "Content-Type: application/json" -H "X-Auth-Token: demo" -H "X-Auth-User: demo" -H "X-Auth-Project: b9f10eca66ac4c279c139d01e65f96b4"
#############################################################################

# Get Ubuntu base image
FROM ubuntu:16.04

# File Author / Maintainer
MAINTAINER Sulochan Acharya

# Install required software and tools
RUN apt-get update \
    && apt-get install -y \
    gcc \
    git \
    curl \
    build-essential \
    python3.5 \
    python3.5-dev

# Get pip
ADD https://bootstrap.pypa.io/get-pip.py /root/get-pip.py

# Install pip
RUN python3.5 /root/get-pip.py

# Install Mariadb
RUN apt-get install -y mariadb-server mariadb-client

# Install MySQL-python
RUN apt-get install -y libmysqlclient-dev python-mysqldb

# pip install virtualenv
RUN pip3 install virtualenv

# Expose port
EXPOSE 8080 3306

Add ./requirements.txt /requirements.txt

# Init virutalenv
RUN virtualenv -p /usr/bin/python3.5 /craton

# Change Working Dir
WORKDIR /craton

# Install requirements
RUN bin/pip install -r /requirements.txt

# pip install mysql-python
RUN bin/pip install mysqlclient

# Add Craton
ADD . /craton

# Install Craton
RUN bin/pip install .

CMD ["tools/docker_run.sh"]
