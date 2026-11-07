BEGIN { a["x4"]=1; a["y4"]=2; total=0; for(k in a) total+=a[k]; print total; delete a["x4"]; print ("x4" in a), ("y4" in a) }
