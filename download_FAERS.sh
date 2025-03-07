#!/bin/bash

# Function to download and extract
download_and_extract() {
    local url="$1"
    local filename="$(basename "$url")"

    echo "Downloading $filename from $url..."
    wget -qc "$url"

    if [[ $? -ne 0 ]]; then
        echo "Failed to download $filename" >> error.log
        return 1
    fi

    echo "Extracting $filename..."

    unzip -Lj "$filename" "ascii/*.txt" && rm -f "$filename" 

    echo "Completed: $filename"
}

export -f download_and_extract 

        
start_year=2014
start_quarter=3
end_year=2023
end_quarter=4
mkdir -p data && cd data

base_url="https://fis.fda.gov/content/Exports"
for year in $(seq $start_year $end_year); do
    for quarter in {1..4}; do
        # Ensure we start from 2014-Q3 and end at 2023-Q4
        if [[ ("$year" -gt $start_year) || ("$year" -eq $start_year && "$quarter" -ge $start_quarter) ]]; then
            if [[ ("$year" -lt $end_year) || ("$year" -eq $end_year && "$quarter" -le $end_quarter) ]]; then
                url="$base_url/faers_ascii_${year}q${quarter}.zip"

                # Check if file exists on the server
                if curl --head --silent --fail "$url" > /dev/null; then
                    download_and_extract "$url" &
                fi
            fi
        fi
    done
done

wait  