BEGIN { a["x1"]=1; a["y1"]=2; total=0; for(k in a) total+=a[k]; print total; delete a["x1"]; print ("x1" in a), ("y1" in a) }
