BEGIN { x="ab"; sub(/a|ab/,"Z",x); print x }
