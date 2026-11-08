BEGIN { split("10 9 abc", A); print (A[1] > A[2]), (A[3] > A[1]), ("10" > "9") }
