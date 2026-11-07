BEGIN { FS=":"; OFS="|" } { $3="x2"; print NF,$0 }
