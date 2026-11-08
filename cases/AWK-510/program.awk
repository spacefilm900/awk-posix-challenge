BEGIN { CONVFMT = "%.2g"; OFMT = "%.4f"; x = 3.14159; a[x] = 1; for (k in a) print k; print x; print x ""; print 17 "" }
