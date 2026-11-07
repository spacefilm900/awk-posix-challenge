BEGIN { print "first4" > "out.txt"; close("out.txt"); print "second4" >> "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
