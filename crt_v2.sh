#!/bin/bash

# Display banner


Help() {
    echo "Options:"
    echo ""
    echo "-h     Help"
    echo "-d     Search Domain Name       | Example: $0 -d hackerone.com"
    echo "-o     Search Organization Name | Example: $0 -o hackerone+inc"
    echo ""
}

CleanResults() {
    sed 's/\\n/\n/g' | \
    sed 's/\*.//g' | \
    sed -r 's/([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})//g' | \
    sort | uniq
}

Domain() {
    if [ -z "$req" ]; then
        echo "Error: Domain name is required."
        exit 1
    fi

    # Encode request properly
    encoded_req=$(printf "%s" "$req" | sed 's/\./%25./g')
    
    # Get response
    response=$(curl -s "https://crt.sh?q=%25.$encoded_req&output=json")

    # Check if response starts with [ (valid JSON array)
    if [[ "$response" != \[* ]]; then
        echo "Error: Unexpected response format. Response was:"
        echo "$response" | head -n 5
        exit 1
    fi

    # Parse and clean
    results=$(echo "$response" | jq -r ".[].common_name,.[].name_value" | CleanResults)

    if [ -z "$results" ]; then
        echo "No valid results found."
        exit 1
    fi

    echo "$results"

}

Organization() {
    if [ -z "$req" ]; then
        echo "Error: Organization name is required."
        exit 1
    fi

    response=$(curl -s "https://crt.sh?q=$req&output=json")

    if [[ "$response" != \[* ]]; then
        echo "Error: Unexpected response format. Response was:"
        echo "$response" | head -n 5
        exit 1
    fi

    results=$(echo "$response" | jq -r ".[].common_name" | CleanResults)

    if [ -z "$results" ]; then
        echo "No valid results found."
        exit 1
    fi

    echo ""
    echo "$results"
    echo ""
    echo -e "[✅] Done"
}

# Main
if [ -z "$1" ]; then
    Help
    exit
fi

while getopts "h:d:o:" option; do
    case $option in
        h) Help ;;
        d) req=$OPTARG; Domain ;;
        o) req=$OPTARG; Organization ;;
        *) Help ;;
    esac
done
