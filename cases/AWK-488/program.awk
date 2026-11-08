BEGIN { match("abc", /b/); a = RSTART " " RLENGTH; match("abc", /z/); print a, RSTART, RLENGTH }
