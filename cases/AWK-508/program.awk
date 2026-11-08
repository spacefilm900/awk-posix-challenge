BEGIN { OFS = "-" } { $(NF + 2) = "z"; print; print NF }
