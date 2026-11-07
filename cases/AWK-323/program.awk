BEGIN { FS=":"; OFS="|" } { $3="x3"; print NF,$0 }
