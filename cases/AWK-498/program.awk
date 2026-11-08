BEGIN { n = split(":a::b:", A, /:/); print n, "[" A[1] "]", "[" A[3] "]", "[" A[5] "]" }
