BEGIN{FS=",";OFS="|"}{sub(/b/,"X",$2);print $0 ":" NF}
