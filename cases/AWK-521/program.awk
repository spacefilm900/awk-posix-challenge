BEGIN { s="abc"; n=sub(/bc|a/,"X",s); print n,s }
