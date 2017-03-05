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

####################################
# Create initial project and users #
####################################

# TODO(jimbaker) should do this via SQLAlchemy models to construct
# bootstrap project/user (use models to ensure constraints are
# satisfied); then add other users via REST API

cat <<EOF | mysql  --user=root craton
insert into variable_association (created_at, updated_at, discriminator) values (NOW(), NOW(), 'project');
insert into projects (created_at, updated_at, name, variable_association_id, id) values (NOW(), NOW(), '$USERNAME', LAST_INSERT_ID(), '$PROJECT');
insert into variable_association (created_at, updated_at, discriminator) values (NOW(), NOW(), 'user');
INSERT into users (created_at, updated_at, project_id, username, api_key, is_root, is_admin, variable_association_id) values (NOW(), NOW(), '$PROJECT', '$BOOTSTRAP_USERNAME', '$BOOTSTRAP_TOKEN', True, False, LAST_INSERT_ID());
insert into variable_association (created_at, updated_at, discriminator) values (NOW(), NOW(), 'user');
INSERT into users (created_at, updated_at, project_id, username, api_key, is_root, is_admin, variable_association_id) values (NOW(), NOW(), '$PROJECT', '$USERNAME', '$TOKEN', False, False, LAST_INSERT_ID());
insert into variable_association (created_at, updated_at, discriminator) values (NOW(), NOW(), 'user');
INSERT into users (created_at, updated_at, project_id, username, api_key, is_root, is_admin, variable_association_id) values (NOW(), NOW(), '$PROJECT', '$ADMIN_USERNAME', '$ADMIN_TOKEN', False, True, LAST_INSERT_ID());
insert into variable_association (created_at, updated_at, discriminator) values (NOW(), NOW(), 'user');
INSERT into users (created_at, updated_at, project_id, username, api_key, is_root, is_admin, variable_association_id) values (NOW(), NOW(), '$PROJECT', '$ROOT_USERNAME', '$ROOT_TOKEN', True, True, LAST_INSERT_ID());
EOF

#########################
# Start the API service #
#########################
/craton/bin/craton-api --config-file=/craton/etc/craton-api-conf.sample
