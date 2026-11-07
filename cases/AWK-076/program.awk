function change(a) { a["k"]="new" } BEGIN { x["k"]="old"; change(x); print x["k"] }
