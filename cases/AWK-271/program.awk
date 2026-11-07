{ print FILENAME, NR, FNR, $1 } END { print "end",NR,FNR,FILENAME }
