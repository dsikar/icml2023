#!/bin/bash

# Check if a file name is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# File name is the first argument
FILE="$1"

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "File not found: $FILE"
    exit 1
fi

# Use grep to find lines matching the pattern (with any year) and sed to extract the title
grep -o '<li><a href=\"/virtual/[0-9]\{4\}/poster/[^\"]*\">[^<]*</a></li>' "$FILE" | sed 's/.*>\(.*\)<\/a><\/li>/\1/'


