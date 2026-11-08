BEGIN { A[1]; A[2]; A["x"]; delete A; print length(A), (1 in A); A["y"] = 5; print length(A), A["y"] }
