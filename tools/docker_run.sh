#!/bin/bash

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

mysql -uroot -e "SET GLOBAL log_output = 'TABLE';SET GLOBAL general_log = 'ON';"
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
# NOTE(sulo): One initial bootstrap project with root user will be created by the
# bootstrap process. Users can docker logs -f <container-id> to view their api-key
# to use with the client.
/craton/bin/craton-dbsync --config-file=etc/craton-api-conf.sample bootstrap

#########################
# Start the API service #
#########################
/craton/bin/craton-api --config-file=/craton/etc/craton-api-conf.sample
