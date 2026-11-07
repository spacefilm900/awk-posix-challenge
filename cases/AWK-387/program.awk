BEGIN { a["x2"]=1; a["y2"]=2; total=0; for(k in a) total+=a[k]; print total; delete a["x2"]; print ("x2" in a), ("y2" in a) }
