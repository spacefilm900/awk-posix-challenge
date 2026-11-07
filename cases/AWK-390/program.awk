BEGIN { a["x5"]=1; a["y5"]=2; total=0; for(k in a) total+=a[k]; print total; delete a["x5"]; print ("x5" in a), ("y5" in a) }
