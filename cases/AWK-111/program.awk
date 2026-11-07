BEGIN{OFS="/"}{NF=1;$3="x";print NF ":" $0}
