BEGIN{s="abc123";match(s,/[0-9]+/);print substr(s,RSTART,RLENGTH)}
