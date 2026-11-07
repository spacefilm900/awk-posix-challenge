BEGIN{RS="";FS="[,;]"}{print NF ":" $1 ":" $NF}
