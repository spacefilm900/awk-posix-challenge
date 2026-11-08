function fill(arr) { arr["x"] = 1 } BEGIN { fill(A); print length(A), A["x"] }
