BEGIN { c = "cat >/dev/null; exit 3"; print "x" | c; r = close(c); print (r != 0) }
