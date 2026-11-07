BEGIN { FS=","; a[1]="old"; split("x2:y2",a,":"); print length(a),a[1],a[2] }
