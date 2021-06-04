#!/usr/bin/awk -f

BEGIN{
        print "    \"arp\": {\n       \"columns\": [\"interface\", \"macAddr\", \"ipAddr\"],\n          \"rows\": ["
}

# ignore lines that don't start with an IP address
/^[0-9]/{
	print "            [\""$3"\",\""$2"\", \""$1"\"]"
}

END{
        print "         ]\n    },"
}

