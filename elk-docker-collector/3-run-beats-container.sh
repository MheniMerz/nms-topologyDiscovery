#!/bin/sh

# filebeat
sudo docker pull docker.elastic.co/beats/filebeat:7.6.2
sudo docker run \
	--restart always --name filebeat -it\
	docker.elastic.co/beats/filebeat:7.6.2 \
	setup -E setup.kibana.host=172.17.0.2:5601 \
	-E output.elasticsearch.hosts=["172.17.0.2:9200"]

# packetbeat
sudo docker pull docker.elastic.co/beats/packetbeat:8.0.0
sudo docker run \
	--restart always --name pakcetbeat -it\
	docker.elastic.co/beats/packetbeat:8.0.0 \
	setup -E setup.kibana.host=172.17.0.2:5601 \
	-E output.elasticsearch.hosts=["172.17.0.2:9200"]

