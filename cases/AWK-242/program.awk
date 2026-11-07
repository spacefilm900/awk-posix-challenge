function inc(a){a[2]=toupper(a[2])}BEGIN{split("a:b:c",a,":");inc(a);print a[1] a[2] a[3]}
