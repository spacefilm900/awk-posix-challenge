BEGIN { FS="," } { OFS="^"; print $0; $1=$1; print $0 }
