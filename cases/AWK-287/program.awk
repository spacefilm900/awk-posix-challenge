BEGIN {print "begin",v} {print v,$1,FILENAME} END {print "end",v}
