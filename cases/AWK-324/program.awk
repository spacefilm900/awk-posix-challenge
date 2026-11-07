BEGIN { FS=":"; OFS="|" } { $3="x4"; print NF,$0 }
