BEGIN{FS=",";OFS=","}{$2="B";$0=$0 ",D";print NF ":" $3 ":" $4}
