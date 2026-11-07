BEGIN { print "one5" > "out.txt"; print "two5" > "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
