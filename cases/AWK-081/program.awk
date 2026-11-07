function f(a) { a[1]++; a[2]++ } BEGIN { x[1]=4; f(x); print x[1] ":" x[2] }
