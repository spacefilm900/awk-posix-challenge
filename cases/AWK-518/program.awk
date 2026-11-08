BEGIN { n=0; x=(1 ? 5 : (n=1)); y=(0 ? (n=2) : 7); print x,y,n }
