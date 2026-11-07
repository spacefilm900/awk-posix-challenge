BEGIN{FS=","}{print NF ":" $3 ":" length($3)}
