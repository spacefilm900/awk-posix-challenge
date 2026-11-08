BEGIN { print match("zabcd", /abcd|za/), RLENGTH; s = "zabcd"; sub(/abcd|za/, "<&>", s); print s; print match("abcd", /ab|abcd/), RLENGTH }
