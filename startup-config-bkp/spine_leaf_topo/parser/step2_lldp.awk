#!/bin/bash

#!/usr/bin/awk -f

BEGIN{
	i = 0
        print "    \"lldp\": {\n       \"columns\": [\"localPort\", \"remoteDevice\", \"remotePort\"],\n          \"rows\": ["
}

{
	i = i+1
	if (i>3){
		print "          [\""$1"\",\""$2"\", \""$5"\"],"
	}
}

END{
        print "         ]\n    },"
}

