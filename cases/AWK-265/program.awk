BEGIN { while ((getline v < "extra.txt") > 0) { print "x",v,NR,FNR }; close("extra.txt") } { print "main",NR,FNR,$1 }
