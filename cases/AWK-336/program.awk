BEGIN {FS=":"} { print NF,$1,$2; $0="z1:w"; print NF,$1,$2 }
