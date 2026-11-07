BEGIN { a[1]=2; a[2]=3; delete a[1]; print (1 in a) ":" (2 in a) }
