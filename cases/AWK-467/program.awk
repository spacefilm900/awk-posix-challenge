BEGIN { getline a < "f"; getline b < "f"; close("f"); getline c < "f"; print a, b, c }
