BEGIN { s = "hello"; print substr(s, 2) "|" substr(s, 2, 100) "|" substr(s, 6) "|" substr(s, 5, 1) }
