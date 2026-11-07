BEGIN { FS=":"; OFS="/" } { a=$1; $1="q3"; print substr($0,1,3), NF, a }
