BEGIN { FS=","; OFS=";" } { $0="a,b,c"; print NF,$2; $2="q4"; print $0 }
