BEGIN { FS=":"; OFS="/" } { a=$1; $1="q4"; print substr($0,1,3), NF, a }
