BEGIN{FS=","}{print NF ":" length($1) ":" $2}
