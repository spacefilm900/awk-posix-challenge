function f(x, tmp) { tmp=7; return x+tmp } BEGIN { tmp=2; print f(3) ":" tmp }
