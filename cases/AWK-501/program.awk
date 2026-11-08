BEGIN { for (i = 1; i <= 100; i++) A[i] = i; for (k in A) delete A[k]; print length(A) }
