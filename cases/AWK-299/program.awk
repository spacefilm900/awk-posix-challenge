BEGIN { print "one4" > "out.txt"; print "two4" > "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
