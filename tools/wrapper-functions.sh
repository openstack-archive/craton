
# Example usage. Note that we simply pass through httpie conventions,
# such as nested JSON with :=
# (https://github.com/jkbrzt/httpie#non-string-json-fields)
#
# $ craton-post v1/regions name=HKG
# $ craton-get v1/hosts
# $ craton-put v1/hosts/3 device_type=container
# $ craton-put v1/hosts/3/variables foo=47 bar:='["a", "b", "c"]'
# $ craton-delete v1/hosts/4
#
# Additional commands provided to manage with respect to environment
# variables, docker startup, etc.

# NOTE assumes the installation of httpie so that the http command is available!

fix-url() {
  [[ "$1" =~ ^http ]] && echo $1 || echo "${CRATON_URL}/${1}"
}

craton-get() {
  http "$(fix-url $1)" \
    "Content-Type:application/json" \
    "X-Auth-Token:${OS_PASSWORD}" \
    "X-Auth-User:${OS_USERNAME}" \
    "X-Auth-Project:${OS_PROJECT_ID}"
}

craton-post() {
  http POST "$(fix-url $1)" \
    "Content-Type:application/json" \
    "X-Auth-Token:${OS_PASSWORD}" \
    "X-Auth-User:${OS_USERNAME}" \
    "X-Auth-Project:${OS_PROJECT_ID}" \
    "${@:2}"
}

craton-put() {
  http PUT "$(fix-url $1)" \
    "Content-Type:application/json" \
    "X-Auth-Token:${OS_PASSWORD}" \
    "X-Auth-User:${OS_USERNAME}" \
    "X-Auth-Project:${OS_PROJECT_ID}" \
    "${@:2}"
}

craton-delete() {
  http DELETE "$(fix-url $1)" \
    "Content-Type:application/json" \
    "X-Auth-Token:${OS_PASSWORD}" \
    "X-Auth-User:${OS_USERNAME}" \
    "X-Auth-Project:${OS_PROJECT_ID}" \
    "${@:2}"
}

_craton-extract-env() {
    echo OS_PROJECT_ID=$(echo "$1" | grep 'ProjectId' | awk '{print $2}' | tr -d '\r')
    echo OS_USERNAME=$(echo "$1" | grep 'Username' | awk '{print $2}' | tr -d '\r')
    echo OS_PASSWORD=$(echo "$1" | grep 'APIKey' | awk '{print $2}' | tr -d '\r')
}

craton-docker-env() {
    _craton-extract-env "$(docker logs craton-api)"
    CRATON_PORT=$(sed -nr "/^\[api\]/ { :l /^port[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" ../etc/craton-api-conf.sample)
    echo CRATON_URL=http://$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' craton-api):${CRATON_PORT}
}

craton-direct-env() {
    _craton-extract-env "$(craton-dbsync --config-file=../etc/craton-api-conf.dev bootstrap)"
    CRATON_PORT=$(sed -nr "/^\[api\]/ { :l /^port[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" ../etc/craton-api-conf.dev)
    echo CRATON_URL=http://$(sed -nr "/^\[api\]/ { :l /^host[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" ../etc/craton-api-conf.dev):${CRATON_PORT}
}

craton-start-direct() {
    # NOTE(jimbaker) Assumes MySQL user 'craton' is setup with password 'craton'!!!

    cat <<EOF | mysql --user=craton --password=craton
drop database craton;
create database craton CHARACTER SET='utf8';
EOF

    python3 -m pip install -e ..
    python3 -m pip install pymysql
    craton-dbsync --config-file=../etc/craton-api-conf.dev upgrade
    craton-dbsync --config-file=../etc/craton-api-conf.dev bootstrap

    echo "Starting API server..."
    craton-api --config-file=../etc/craton-api-conf.dev
}

craton-reload() {
    echo "Starting API server..."
    craton-api --config-file=../etc/craton-api-conf.dev
}

craton-fake-data() {
    until craton-get v1/regions 2>/dev/null
    do
	echo "Waiting for API server"; sleep 1
    done

    python3 generate_fake_data.py \
	--url $CRATON_URL/v1 \
	--user $OS_USERNAME --project $OS_PROJECT_ID --key $OS_PASSWORD

    craton-get v1/regions
}

craton-start-docker() {
    echo "Starting Craton docker container..."
    docker rm -f craton-api 2>/dev/null || true
    docker build --pull -t craton-api:latest ..
    docker run -t --name craton-api -p 127.0.0.1:7780:7780 -d craton-api:latest

    CRATON_PORT=$(sed -nr "/^\[api\]/ { :l /^port[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" ../etc/craton-api-conf.sample)
    CRATON_URL=http://$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' craton-api):${CRATON_PORT}
    OS_PROJECT_ID=probe
    OS_USERNAME=probe
    OS_PASSWORD=probe
    until craton-get v1/regions 2>/dev/null
    do
	echo "Waiting for API server"; sleep 1
    done

    eval $(craton-docker-env)
    craton-fake-data

    docker logs -f craton-api
}
