BEGIN { x="aaaa"; sub(/a+/,"Z",x); print x }
