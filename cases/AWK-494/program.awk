BEGIN { A[1] = "old"; A[9] = "x"; n = split("p q", A); print n, length(A), (9 in A) }
