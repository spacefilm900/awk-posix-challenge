BEGIN { cmd="printf '4\n5\n'"; r=(cmd | getline x); print r,x,NR; r=(cmd | getline y); print r,y,NR;close(cmd) }
