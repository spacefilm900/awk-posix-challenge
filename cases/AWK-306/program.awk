BEGIN { print "first1" > "out.txt"; close("out.txt"); print "second1" >> "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
