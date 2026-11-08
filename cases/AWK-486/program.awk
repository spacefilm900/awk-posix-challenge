BEGIN { print match("abc", /x*/), RSTART, RLENGTH }
