BEGIN { FS="," } { FS=":"; $0="p:q:r"; print NF,$2 }
