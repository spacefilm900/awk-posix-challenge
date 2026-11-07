BEGIN { FS=","; a[1]="old"; split("x5:y5",a,":"); print length(a),a[1],a[2] }
