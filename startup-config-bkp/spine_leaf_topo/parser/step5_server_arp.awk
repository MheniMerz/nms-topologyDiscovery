#!/usr/bin/awk -f

BEGIN{
        print "    \"arp\": {\n       \"columns\": [\"interface\", \"macAddr\", \"ipAddr\",\"vlan\"],\n          \"rows\": ["
}

(NR>2) {print "            [\""$5"\",\""$3"\", \""$1"\",\"-\"]," }

END{
        print "         ]\n    },"
}
