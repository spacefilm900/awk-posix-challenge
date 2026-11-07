BEGIN { x=5; a[x]="present"; print (x in a), (x "" in a); delete a[x]; print (x in a) }
