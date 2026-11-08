BEGIN { ARGV[1] = "-"; ARGC = 2 } { print FILENAME, $0 }
