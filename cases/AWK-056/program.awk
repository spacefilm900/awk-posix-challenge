BEGIN { FS=","; OFS="|" } { $2="Y"; print $1,$2,$3 }
