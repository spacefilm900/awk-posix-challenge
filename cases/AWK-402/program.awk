BEGIN{OFS="|"}{r=getline $2 < "other"; print r, $0, NF}
