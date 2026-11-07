BEGIN { x="abc"; sub(/ab|abc/,"X",x); print x }
