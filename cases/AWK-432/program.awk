BEGIN{FS=",";OFS="|"}{getline $3 < "other";print $0 ":" NF}
