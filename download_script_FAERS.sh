#!/bin/bash

start_year=2012
end_year=2023
mkdir data
cd data
base_url="https://fis.fda.gov/content/Exports"
for year in $(seq $start_year $end_year); do
	for quarter in {1..4}; do
		url="$base_url/faers_ascii_${year}q${quarter}.zip"
		# Check if the file exists on the server
		if ! curl --head --silent --fail "$url" > /dev/null; then
        		continue
    		fi
    		curl -O "$url"
		echo $url
	done
done
