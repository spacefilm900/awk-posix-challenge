BEGIN { print "one1" > "out.txt"; print "two1" > "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
