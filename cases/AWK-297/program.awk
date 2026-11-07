BEGIN { print "one2" > "out.txt"; print "two2" > "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
