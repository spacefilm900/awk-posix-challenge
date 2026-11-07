BEGIN { x="cat"; sub(/at/,"[&]",x); print x }
