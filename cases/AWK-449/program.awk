BEGIN { print "B[" x "]" } { print "R[" x "]" } END { print "E[" x "]" }
