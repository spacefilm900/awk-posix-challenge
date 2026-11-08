BEGIN { match("abc", /c/); s = "a"; sub(/a/, "x", s); t = "b"; gsub(/b/, "y", t); n = split("a b", A); print RSTART, RLENGTH, index("abc", "a") }
