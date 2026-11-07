BEGIN{RS=";"}{print NR ":" length($0)}
