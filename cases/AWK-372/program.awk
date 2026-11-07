BEGIN { cmd="printf '2\n3\n'"; r=(cmd | getline x); print r,x,NR; r=(cmd | getline y); print r,y,NR;close(cmd) }
