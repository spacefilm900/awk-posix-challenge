BEGIN { a["x3"]=1; a["y3"]=2; total=0; for(k in a) total+=a[k]; print total; delete a["x3"]; print ("x3" in a), ("y3" in a) }
