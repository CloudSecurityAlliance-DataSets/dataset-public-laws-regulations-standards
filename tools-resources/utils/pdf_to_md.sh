#!/bin/bash
# PDF -> markdown via marker. Uses an isolated venv at ~/.venvs/marker/ to
# avoid the chronic transformers/tokenizers/torch dep conflicts that occur
# when marker shares a venv with other ML tooling.
#
# To (re)build the venv:
#   python3 -m venv ~/.venvs/marker
#   ~/.venvs/marker/bin/pip install --upgrade pip
#   ~/.venvs/marker/bin/pip install marker-pdf

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 filename.pdf [output_dir]"
  exit 1
fi

MARKER="${MARKER_BIN:-$HOME/.venvs/marker/bin/marker_single}"
if [ ! -x "$MARKER" ]; then
  echo "marker_single not found at $MARKER"
  echo "Build the venv (see header of this script) or set MARKER_BIN."
  exit 1
fi

OUTPUT_DIR="${2:-./}"

"$MARKER" "$1" \
  --output_format markdown \
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
  --output_dir "$OUTPUT_DIR"
