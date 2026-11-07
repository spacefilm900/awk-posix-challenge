BEGIN {FS=":"} { print NF,$1,$2; $0="z3:w"; print NF,$1,$2 }
