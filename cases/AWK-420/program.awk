BEGIN{RS=":"} NR==1{RS=";"}{print NR ":" $0}
