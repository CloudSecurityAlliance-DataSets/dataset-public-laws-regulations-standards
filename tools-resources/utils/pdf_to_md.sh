#!/bin/bash

# Check if PDF filename is provided
if [ -z "$1" ]; then
  echo "Usage: $0 filename.pdf"
  exit 1
fi

# Corrected marker_single invocation (without processors argument)
marker_single "$1" \
  --output_format markdown \
  --enable_table_ocr \
  --extract_images true \
  --disable_links \
  --disable_multiprocessing \
  --force_ocr \
  --strip_existing_ocr \
  --common_element_threshold 0.2 \
  --common_element_min_blocks 3 \
  --max_streak 3 \
  --text_match_threshold 90 \
  --min_lines_in_block 4 \
  --min_line_length 10 \
  --output_dir ./
