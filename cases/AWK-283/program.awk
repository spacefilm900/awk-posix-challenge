FNR==1 { print FILENAME,NR } { if(FNR==1) nextfile; print $0 } END {print "count",NR}
