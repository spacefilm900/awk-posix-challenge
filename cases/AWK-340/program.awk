BEGIN {FS=":"} { print NF,$1,$2; $0="z5:w"; print NF,$1,$2 }
