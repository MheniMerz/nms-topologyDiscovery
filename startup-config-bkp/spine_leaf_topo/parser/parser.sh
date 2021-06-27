#!/bin/bash
pwd
# parse step1_show interface
RESULT=../error_scenario/duplicate_mac/output.json
echo "{" > $RESULT
for file in ../error_scenario/duplicate_mac/*/; do
	src_host=`cut -d/ -f4 <<< $(echo $file)`
	echo '"'"$src_host"'": {' >> $RESULT;
	if [[ $src_host == *"server"* ]];
	then
		awk -f ./step1_server_interfaces.awk ../error_scenario/duplicate_mac/$src_host/*ip_addr* >> $RESULT;
		awk -f ./step5_server_arp.awk ../error_scenario/duplicate_mac/$src_host/*arp* >> $RESULT;
		awk -f ./step7_server_iproute.awk ../error_scenario/duplicate_mac/$src_host/*ip_route* >> $RESULT;
	else
		awk -f ./step1_interfaces.awk ../error_scenario/duplicate_mac/$src_host/*interface* >> $RESULT;
		awk -f ./step1_vlans.awk ../error_scenario/duplicate_mac/$src_host/*vlan* >> $RESULT;
		awk -f ./step2_lldp.awk ../error_scenario/duplicate_mac/$src_host/*lldp* >> $RESULT;
		awk -f ./step5_arp.awk ../error_scenario/duplicate_mac/$src_host/*arp* >> $RESULT;
		awk -f ./step7_iproute.awk ../error_scenario/duplicate_mac/$src_host/*route* >> $RESULT;
	fi
	echo '},' >> $RESULT
done;
echo " }" >> $RESULT
