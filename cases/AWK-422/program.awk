BEGIN{print "a" > "out";close("out");print "b" > "out";close("out")}
