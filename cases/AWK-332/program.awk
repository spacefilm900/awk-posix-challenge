BEGIN { FS="," } { old=$0; OFS="|"; print old; $1=$1; print $0 }
