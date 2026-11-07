BEGIN {FS=":"} { print NF,$1,$2; $0="z4:w"; print NF,$1,$2 }
