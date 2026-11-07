BEGIN { cmd="printf 'one1\ntwo1\n'"; for(i=1;i<=2;i++){ r=(cmd | getline v); print r,v,NR }; close(cmd); r=(cmd | getline v); print r,v,NR;close(cmd) }
