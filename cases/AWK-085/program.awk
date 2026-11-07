BEGIN { x="abc123def"; print match(x,/[0-9]+/) ":" RSTART ":" RLENGTH }
