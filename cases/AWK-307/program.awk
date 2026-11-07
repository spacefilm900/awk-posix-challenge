BEGIN { print "first2" > "out.txt"; close("out.txt"); print "second2" >> "out.txt"; close("out.txt"); while((getline v < "out.txt") > 0) print v; close("out.txt") }
