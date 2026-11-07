BEGIN{print "hello" > "out";close("out");getline v < "out";close("out");print v}
