#!/usr/bin/awk -f

BEGIN{
	i = 1
        print "    \"ipRoute\": {\n       \"columns\": [\"interface\", \"via\", \"to\", \"type\"],\n          \"rows\": ["
}

# for lines that start with route codes, extract wanted values
/^[A-Z]>/ {
        interface = substr($6, 1, length($6)-1);
	via = substr($5, 1, length($5)-1);
        to = $2;
        type = $1;
}

# for routes for the same target subnet, keep to and type records from the last line
/^\s+\*/ {
        interface = substr($4, 1, length($4)-1);
	via = substr($3, 1, length($3)-1);
}

# print one row
{
	i = i + 1
	if (i>7){
		print "            [\""interface"\",\""via"\",\""to"\",\""type"\"],";
	}
}

END{
        print "         ]\n    },"
}

