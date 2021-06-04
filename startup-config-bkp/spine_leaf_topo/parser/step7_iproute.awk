#!/usr/bin/awk -f

BEGIN{
        print "    \"ipRoute\": {\n       \"columns\": [\"interface\", \"via\", \"to\", \"type\"],\n          \"rows\": ["
}

# for lines that start with route codes, extract wanted values
/^[A-Z]>/ {
        interface = $6;
	via = $5;
        to = $2;
        type = $1;
}

# for routes for the same target subnet, keep to and type records from the last line
/^\s+\*/ {
        via = $3;
	interface = $4;
}

# print one row
{
        print "            [\""interface"\",\""via"\",\""to"\",\""type"\"]";
}

END{
        print "         ]\n    },"
}

