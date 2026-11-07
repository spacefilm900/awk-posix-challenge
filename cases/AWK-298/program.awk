BEGIN { print "one3" > "out.txt"; print "two3" > "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
