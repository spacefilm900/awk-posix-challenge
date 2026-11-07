BEGIN { print "first5" > "out.txt"; close("out.txt"); print "second5" >> "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
