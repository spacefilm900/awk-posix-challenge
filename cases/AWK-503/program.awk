BEGIN { print "b"; exit 2 } { print "main" } END { print "e" }
