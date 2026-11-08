BEGIN { print match("abc", /$/), RSTART, RLENGTH }
