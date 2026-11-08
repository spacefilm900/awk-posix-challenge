BEGIN { a = system("exit 3"); b = system("true"); c = system("false"); print a, b, c }
