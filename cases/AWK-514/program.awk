FNR == 2 { nextfile } { print FILENAME, FNR, NR } END { print NR }
