BEGIN { r = (getline l < "no-such-file"); print r, NR, "[" l "]" }
