BEGIN { print match("\303\251\303\251ab", /ab/), RLENGTH; print match("x\303\251", /\303\251/), RLENGTH }
