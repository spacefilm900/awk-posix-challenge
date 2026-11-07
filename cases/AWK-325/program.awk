BEGIN { FS=":"; OFS="|" } { $3="x5"; print NF,$0 }
