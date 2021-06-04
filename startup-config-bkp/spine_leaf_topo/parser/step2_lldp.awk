#!/bin/bash

#!/usr/bin/awk -f

BEGIN{
	i = 1
        print "\n    \"lldp\": {\n       \"columns\": [\"localPort\", \"remoteDevice\", \"remotePort\", ],\n          \"rows\": ["
}

(NR>3) {
	print "            [\""$1"\",\""$2"\", \""$5"\"]" 
}

END{
        print "         ]\n    },"
}

