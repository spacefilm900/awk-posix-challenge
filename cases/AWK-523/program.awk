BEGIN { a["x"]=1; a["y"]=2; delete a["x"]; print ("x" in a),("y" in a),length(a) }
