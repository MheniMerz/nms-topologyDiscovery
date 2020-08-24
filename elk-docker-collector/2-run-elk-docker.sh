#!/bin/sh

# run the elk docker container
#  1- bind host machine ports to the container ports
#      5044--> logstash
#      5601 --> kibana
#      9200 --> elasticsearch
#  2- --restart always --> make container start on boot
sudo docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --restart always --name elk sebp/elk
