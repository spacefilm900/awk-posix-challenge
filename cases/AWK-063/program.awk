BEGIN { print "BEGIN" } { n++; if (n==1) print "BODY" } END { print "END:" n }
