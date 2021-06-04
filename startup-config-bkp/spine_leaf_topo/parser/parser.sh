#!/bin/bash
pwd
# parse step1_show interface
RESULT=./output.json
echo '{' > $RESULT
for file in ../*/; do
	src_host=`cut -d/ -f2 <<< $(echo $file)`
	echo '"'"$src_host"'": {' >> $RESULT;
	if [[ $src_host == *"server"* ]];
	then
		awk -f ./step1_server_interfaces.awk ../$src_host/*ip_addr* >> $RESULT;
		awk -f ./step5_server_arp.awk ../$src_host/*arp* >> $RESULT;
		awk -f ./step7_server_iproute.awk ../$src_host/*ip_route* >> $RESULT;
	else
		awk -f ./step1_interfaces.awk ../$src_host/*interface* >> $RESULT;
		awk -f ./step1_vlans.awk ../$src_host/*vlan* >> $RESULT;
		awk -f ./step2_lldp.awk ../$src_host/*lldp* >> $RESULT;
		awk -f ./step5_arp.awk ../$src_host/*arp* >> $RESULT;
		awk -f ./step7_iproute.awk ../$src_host/*route* >> $RESULT;
	fi
	echo '},' >> $RESULT
done;
echo '}' >> $RESULT
