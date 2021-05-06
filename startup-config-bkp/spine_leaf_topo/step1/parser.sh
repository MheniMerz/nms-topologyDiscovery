#!/bin/bash

# doesn't do a perfect job

for file in ./*; do
	filename=`cut -d/ -f2 <<< $(echo $file)`
	src_host=`cut -d_ -f1 <<< $(echo $filename)`
	[[ $src_host == "parser.sh" ]] || awk '(NR>3) {print "{ host: '"$src_host"', name: "$1"},"}' $file >> output
	echo >> output
done;
