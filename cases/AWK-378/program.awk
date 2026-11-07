BEGIN { FS=","; a[1]="old"; split("x3:y3",a,":"); print length(a),a[1],a[2] }
