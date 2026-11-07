BEGIN { cmd="printf '3\n4\n'"; r=(cmd | getline x); print r,x,NR; r=(cmd | getline y); print r,y,NR;close(cmd) }
