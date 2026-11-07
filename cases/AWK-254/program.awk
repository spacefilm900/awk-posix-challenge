BEGIN { r=getline; print r,NR,FNR,$1,NF } { print "rule",NR,$1 }
