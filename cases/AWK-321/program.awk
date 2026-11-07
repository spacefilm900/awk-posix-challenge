BEGIN { FS=":"; OFS="|" } { $3="x1"; print NF,$0 }
