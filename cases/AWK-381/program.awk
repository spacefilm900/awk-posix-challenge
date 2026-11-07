BEGIN { OFS="|"; a="ab"; gsub(/a|ab/,"X",a); print a }
