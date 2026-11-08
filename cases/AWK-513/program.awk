FNR == 1 { while ((getline l < FILENAME) > 0) n++; close(FILENAME) } END { print n, NR }
