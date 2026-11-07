BEGIN { cmd="printf '5\n6\n'"; r=(cmd | getline x); print r,x,NR; r=(cmd | getline y); print r,y,NR;close(cmd) }
