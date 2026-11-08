BEGIN { print "x" > "out"; a = close("out"); b = close("out"); print a, (b != 0) }
