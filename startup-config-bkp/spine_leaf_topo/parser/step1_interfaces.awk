#!/usr/bin/awk -f

BEGIN{
	print "    \"interface\": {\n       \"columns\": [\"name\", \"macAddr\", \"ipAddr\", \"type\"],\n          \"rows\": ["
}

# first line extract interface_name and initialize other variables
/^Interface/ {
	interface_name = $2;
	mac_addr = "-";
	ip_addr = "-";
	type = "-";
}

/^.+HWaddr/ {
	for (x=1;x<=NF;x++) 
		if ($x~"HWaddr")  
			mac_addr = $(x+1);
}

/^\s+inet\s/ {
	ip_addr = $2;
}

# get interface type and print one row
/^\s+Interface\sType/ {
	type = $3;	
	print "            [\""interface_name"\",\""mac_addr"\",\""ip_addr"\",\""type"\"],";
		
}

END{
	print "         ]\n    },"	
}
