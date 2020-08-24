#!/bin/bash

# 1- build (run once)
sudo docker build --tag ddos-attack .
# 2- run
sudo docker run -dit --name ddos-attack222 --restart=always --net=222 ddos-attack
sudo docker run -dit --name ddos-attack225 --restart=always --net=225 ddos-attack
sudo docker run -dit --name ddos-attack220 --restart=always --net=220 ddos-attack
