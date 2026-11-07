BEGIN { print "begin" } { print "record", $0 } END { print "end" }
