BEGIN { CONVFMT="%.2f"; k=5/10; a[k]="ok"; printf "%s:%s\n", a[sprintf("%.2f",k)], k "" }
