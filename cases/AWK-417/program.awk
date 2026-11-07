BEGIN{RS="";FS="a"}{print NF ":" $1 ":" $NF}
