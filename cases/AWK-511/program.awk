FNR == 1 { print FILENAME, NR } END { print FILENAME, NR, FNR }
