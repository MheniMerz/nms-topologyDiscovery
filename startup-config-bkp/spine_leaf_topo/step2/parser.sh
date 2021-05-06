#!/bin/bash

# doesn't do a perfect job
# after running this, we need to remove entries for parser
# and remove last 2 entries for each host

for file in ./*; do
	filename=`cut -d/ -f2 <<< $(echo $file)`
	src_host=`cut -d_ -f1 <<< $(echo $filename)`
	awk '(NR>3) {print "{ srcHost: '"$src_host"', srcInterface: "$1", destHost: "$2", destInterface: "$5" },"}' $file >> output
	echo >> output
done;
