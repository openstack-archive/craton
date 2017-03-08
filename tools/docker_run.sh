#!/bin/bash

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

mysql -uroot -e "CREATE DATABASE craton CHARACTER SET = 'utf8'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON craton.* TO 'craton'@'%' IDENTIFIED BY 'craton'"
mysqladmin flush-privileges

###############
# Run db-sync #
##############
/craton/bin/craton-dbsync --config-file=/craton/etc/craton-api-conf.sample upgrade


####################################
# Create initial project and users #
####################################

# Project and Users created as a part of this script is meant
# for testing purposes only. Users can try out craton service
# by using these credentials along with Dockerfile.

PROJECT="b9f10eca66ac4c279c139d01e65f96b4"

BOOTSTRAP_USERNAME="bootstrap"
BOOTSTRAP_TOKEN="bootstrap"

USERNAME="demo"
TOKEN="demo"

ADMIN_USERNAME="demo_admin"
ADMIN_TOKEN="demo_admin"

ROOT_USERNAME="demo_root"
ROOT_TOKEN="demo_root"

PROJECT_DISCRIMINATOR='project'

/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap-project --projectname $USERNAME --id $PROJECT
/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap-user --project $PROJECT --username $USERNAME --project $PROJECT --key $TOKEN
/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap-user --project $PROJECT --username $BOOTSTRAP_USERNAME --key $BOOTSTRAP_TOKEN --root true
/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap-user --project $PROJECT --username $ADMIN_USERNAME --project $PROJECT --key $ADMIN_TOKEN --admin true
/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap-user --project $PROJECT --username $ROOT_USERNAME --project $PROJECT --key $ROOT_TOKEN --admin ture --root true

#########################
# Start the API service #
#########################
/craton/bin/craton-api --config-file=/craton/etc/craton-api-conf.sample
