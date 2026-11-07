BEGIN { print "start3" > "out.txt"; close("out.txt"); print "new3" > "out.txt"; close("out.txt"); while((getline x < "out.txt") > 0) print x; close("out.txt") }
