function modify(v) { sub(/b/, "X1", v); return v } BEGIN {FS=":";OFS="|"} { $2=modify($2); print NF,$0 }
