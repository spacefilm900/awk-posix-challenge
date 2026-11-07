BEGIN { FS=","; OFS=";" } { $0="a,b,c"; print NF,$2; $2="q2"; print $0 }
