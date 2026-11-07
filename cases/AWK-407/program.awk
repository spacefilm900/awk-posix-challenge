BEGIN{getline v;print "BEGIN:" v ":" NR} {print "MAIN:" $0 ":" NR}
