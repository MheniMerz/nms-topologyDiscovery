#!/usr/bin/awk -f

BEGIN{
	print "    \"vlan\": {\n       \"columns\": [\"name\", \"vid\", \"member\", \"mode\"],\n          \"rows\": ["
}

(NR>2) {print "            [\""$1"\",\""$2"\", \""$3"\", \""$4"\"]" }

END{
	print "         ]\n    },"	
}
