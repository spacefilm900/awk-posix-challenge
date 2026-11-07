BEGIN { cmd="printf '1\n2\n'"; r=(cmd | getline x); print r,x,NR; r=(cmd | getline y); print r,y,NR;close(cmd) }
