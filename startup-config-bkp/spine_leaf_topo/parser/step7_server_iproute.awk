#!/usr/bin/awk -f

BEGIN{
        print "    \"ipRoute\": {\n       \"columns\": [\"interface\", \"via\", \"to\", \"type\"],\n          \"rows\": ["
}

# for lines that start with route codes, extract wanted values
/^default/ {
        interface = $NF
	via = $3;
        to = "0.0.0.0/0";
        type = "-";
}

# for routes for the same target subnet, keep to and type records from the last line
/^[0-9]/ {
        interface = $3;
	via = $NF;
	to = $1;
	type = "-";
}

# print one row
{
        print "            [\""interface"\",\""via"\",\""to"\",\""type"\"]";
}

END{
        print "         ]\n    },"
}

