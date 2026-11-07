BEGIN{cmd="printf 'x\ny\n'";cmd | getline a;close(cmd);cmd | getline b;print a ":" b;close(cmd)}
