BEGIN { cmd="printf 'one4\ntwo4\n'"; for(i=1;i<=2;i++){ r=(cmd | getline v); print r,v,NR }; close(cmd); r=(cmd | getline v); print r,v,NR;close(cmd) }
