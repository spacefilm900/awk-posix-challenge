BEGIN{cmd="printf 'a\nb\n'";cmd | getline a;cmd | getline b;print a ":" b;close(cmd)}
