BEGIN { s="aba"; print gsub(/a/,"<&>",s),s }
