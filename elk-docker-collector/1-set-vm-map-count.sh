#!/bin/sh
sudo echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sudo sysctl --system
