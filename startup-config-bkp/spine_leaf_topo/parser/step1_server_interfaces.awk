#!/usr/bin/awk -f

BEGIN{
	print "\n    \"interface\": {\n       \"columns\": [\"name\", \"macAddr\", \"ipAddr\", \"type\"],\n          \"rows\": ["
}

# first line extract interface_name and initialize other variables
/^[0-9]+:/ {
	interface_name = substr($2, 1, length($2)-1);
	mac_addr = "-";
	ip_addr = "-";
	type = "-";
}

/^\s+link/ {
	mac_addr = $2;
}

/^\s+inet\s/ {
	ip_addr = $2;
	print "            [\""interface_name"\",\""mac_addr"\",\""ip_addr"\",\""type"\"]";
}

END{
	print "         ]\n    },"	
}
