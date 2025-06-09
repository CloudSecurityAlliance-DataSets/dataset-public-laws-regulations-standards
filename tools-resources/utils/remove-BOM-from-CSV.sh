#!/bin/bash

# Loop through all CSV files in the current directory
for file in *.csv; do
  # Check if the file exists (handles case when no CSV files are present)
  if [[ -f "$file" ]]; then
    # Create a secure temporary file
    tmpfile=$(mktemp)

    # Use sed to remove BOM and write to the temporary file
    sed '1s/^\xEF\xBB\xBF//' "$file" > "$tmpfile"
    
    # Overwrite the original file with the contents of the temp file
    mv "$tmpfile" "$file"
    
    echo "Processed: $file"
  fi
done

echo "All CSV files processed."
