BEGIN { x="ababab"; print sub(/ab/,"x",x) ":" x }
