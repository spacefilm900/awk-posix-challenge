BEGIN { FS=","; a[1]="old"; split("x4:y4",a,":"); print length(a),a[1],a[2] }
