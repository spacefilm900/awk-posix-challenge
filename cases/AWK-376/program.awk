BEGIN { FS=","; a[1]="old"; split("x1:y1",a,":"); print length(a),a[1],a[2] }
