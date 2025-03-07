#!/bin/bash
user = "postgres"
db = "faers"
psql -U $user -d $db -c "\copy DEMO FROM './data/DEMO.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy DRUG FROM './data/DRUG.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy INDI FROM './data/INDI.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy OUTC FROM './data/OUTC.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy REAC FROM './data/REAC.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy RPSR FROM './data/RPSR.csv' DELIMITER ',' CSV HEADER;"

psql -U $user -d $db -c "\copy THER FROM './data/THER.csv' DELIMITER ',' CSV HEADER;"
