function clr(a) { delete a } BEGIN { A[1]; A[2]; clr(A); print length(A); A[3] = 1; print length(A) }
