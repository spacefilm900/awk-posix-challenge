BEGIN { SUBSEP="@"; a["x","y"]=17; print a["x@y"], (("x@y") in a) }
