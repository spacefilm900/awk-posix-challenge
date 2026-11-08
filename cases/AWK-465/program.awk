BEGIN { "echo a" | getline x; print x, close("echo a") }
