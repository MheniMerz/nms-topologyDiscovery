#!/usr/bin/awk -f

BEGIN{
        print "\n    \"arp\": {\n       \"columns\": [\"interface\", \"macAddr\", \"ipAddr\", ],\n          \"rows\": ["
}

(NR>2) {print "            [\""$5"\",\""$3"\", \""$1"\"]" }

END{
        print "         ]\n    },"
}
