BEGIN { FS=","; OFS=";" } { $0="a,b,c"; print NF,$2; $2="q3"; print $0 }
