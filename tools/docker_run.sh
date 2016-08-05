#!/bin/bash

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

mysql -uroot -e "CREATE DATABASE craton CHARACTER SET = 'utf8mb4'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON craton.* TO 'craton'@'%' IDENTIFIED BY 'craton'"
mysqladmin flush-privileges

###############
# Run db-sync #
##############
/craton/bin/craton-inventory-dbsync --config-file=etc/inventory-api-conf.sample upgrade

###################################
# Create initial project and user #
###################################
mysql -u root craton -e "INSERT into projects (created_at, updated_at, name) values (NOW(), NOW(), 'demo')"
mysql -u root craton -e "INSERT into users (created_at, updated_at, project_id, username, api_key, is_admin) values (NOW(), NOW(), 1, 'demo', 'demo', False)"

#########################
# Start the API service #
#########################
/craton/bin/python3.5 /craton/craton/cmd/inventory-api.py --config-file=/craton/etc/inventory-api-conf.sample
