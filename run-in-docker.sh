#!/bin/bash

REGISTRY=image.changhong.com/onecloud
VERSION=fusion.3.9.14.8
OCBOOT_IMAGE="$REGISTRY/ocboot:$VERSION"

if ! docker ps > /dev/null 2>&1; then
    echo "Error: Docker unavailable, Please resolve the problem and try again"
    exit 3
fi

if [ $# -eq 0 ]; then
    docker run --rm $OCBOOT_IMAGE -h
    exit 1
fi

config_dir="$(pwd)/_config"
run_cmd="docker run --rm -t --network host -v $HOME/.ssh/id_rsa:/root/.ssh/id_rsa -v $config_dir:/opt/ocboot/_config -v $(pwd)/VERSION:/opt/ocboot/VERSION --env OCBOOT_CONFIG_DIR=/opt/ocboot/_config --env OFFLINE_DATA_PATH=/opt/offline/"
mkdir -p "$config_dir"

if [ $# -eq 1 ]; then
    $run_cmd --entrypoint /opt/ocboot/run.py $OCBOOT_IMAGE $@
elif [ $# -ge 2 ]; then
    $run_cmd $OCBOOT_IMAGE $@
fi
