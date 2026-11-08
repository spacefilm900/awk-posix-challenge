BEGIN { s = "a\303\251b"; print substr(s, 2, 1), length(s) }
