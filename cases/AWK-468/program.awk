BEGIN { print "a" > "o"; close("o"); print "b" > "o"; close("o"); while ((getline l < "o") > 0) print "got " l }
