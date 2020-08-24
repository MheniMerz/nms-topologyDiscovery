#!/bin/bash
docker network create --driver=bridge oustide --subnet=172.17.0.0/16
docker network create --driver=bridge 222 --subnet=10.11.200.0/26 --opt com.docker.network.bridge.name=docker222
docker network create --driver=bridge 225 --subnet=10.11.200.64/26 --opt com.docker.network.bridge.name=docker225
docker network create --driver=bridge 220 --subnet=10.11.200.128/26 --opt com.docker.network.bridge.name=docker220
