#!/bin/bash
# pdf_to_md_via_gpu.sh — Mac-side wrapper for marker extraction on the GPU box.
#
# Workflow:
#   1. scp the canonical marker-convert.sh to the remote (so any fixes here
#      are picked up automatically — no drift)
#   2. scp the PDF to the remote work dir
#   3. Run marker-convert.sh --ai (detached tmux) on the remote
#   4. Poll the remote log file every N seconds until STATUS: DONE/FAILED
#   5. scp the output directory back, drop into --output-dir
#   6. (Optional) clean up remote files
#
# Usage: pdf_to_md_via_gpu.sh [options] input.pdf [extra marker_single flags...]
#
# Options:
#   --output-dir DIR    Local output parent dir (default: PDF's parent dir).
#                       Results land at <output-dir>/<pdf-basename>/.
#   --formats CSV       Forwarded to marker-convert.sh. Default: markdown.
#   --force-ocr         Forwarded. Default OFF.
#   --remote-host HOST  SSH host (default: markersinglehost).
#   --remote-dir DIR    Remote work directory (default: ~/marker-work).
#   --poll-interval N   Seconds between log polls (default: 30).
#   --timeout SEC       Give up after this many seconds (default: 7200 = 2h).
#   --keep-remote       Don't delete remote files after copy-back.
#   --help, -h          Show this help.

set -euo pipefail

OUTPUT_DIR=""
FORMATS_CSV="markdown"
FORCE_OCR=0
REMOTE_HOST="markersinglehost"
REMOTE_DIR='~/marker-work'
POLL_INTERVAL=30
TIMEOUT=7200
KEEP_REMOTE=0
POSITIONAL=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output-dir)    OUTPUT_DIR="$2"; shift 2 ;;
        --formats)       FORMATS_CSV="$2"; shift 2 ;;
        --force-ocr)     FORCE_OCR=1; shift ;;
        --remote-host)   REMOTE_HOST="$2"; shift 2 ;;
        --remote-dir)    REMOTE_DIR="$2"; shift 2 ;;
        --poll-interval) POLL_INTERVAL="$2"; shift 2 ;;
        --timeout)       TIMEOUT="$2"; shift 2 ;;
        --keep-remote)   KEEP_REMOTE=1; shift ;;
        --help|-h)       awk 'NR>1 && /^#/{sub(/^# ?/,""); print; next} NR>1{exit}' "$0"; exit 0 ;;
        *)               POSITIONAL+=("$1"); shift ;;
    esac
done

set -- "${POSITIONAL[@]:-}"

if [ $# -lt 1 ] || [ -z "${1:-}" ]; then
    echo "Error: No input PDF specified. Run with --help for usage." >&2
    exit 1
fi

INPUT="$(realpath "$1")"
shift

if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT" >&2
    exit 1
fi

BASENAME="$(basename "$INPUT")"
STEM="${BASENAME%.pdf}"
STEM="${STEM%.PDF}"
[ -n "$OUTPUT_DIR" ] || OUTPUT_DIR="$(dirname "$INPUT")"
mkdir -p "$OUTPUT_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_MARKER_SH="$SCRIPT_DIR/marker-convert.sh"

if [ ! -f "$LOCAL_MARKER_SH" ]; then
    echo "Error: marker-convert.sh not found next to this script at $LOCAL_MARKER_SH" >&2
    exit 1
fi

# Extra args forwarded to marker_single (anything after the PDF on the CLI)
EXTRA_ARGS=("$@")

echo "==> Preparing remote work directory on $REMOTE_HOST"
ssh "$REMOTE_HOST" "mkdir -p $REMOTE_DIR"

echo "==> Uploading marker-convert.sh (canonical copy)"
scp -q "$LOCAL_MARKER_SH" "$REMOTE_HOST:$REMOTE_DIR/marker-convert.sh"
ssh "$REMOTE_HOST" "chmod +x $REMOTE_DIR/marker-convert.sh"

echo "==> Uploading PDF: $BASENAME"
scp -q "$INPUT" "$REMOTE_HOST:$REMOTE_DIR/$BASENAME"

# Build remote command
REMOTE_CMD="cd $REMOTE_DIR && ./marker-convert.sh --ai --formats $(printf %q "$FORMATS_CSV")"
if [ "$FORCE_OCR" = "1" ]; then
    REMOTE_CMD="$REMOTE_CMD --force-ocr"
fi
REMOTE_CMD="$REMOTE_CMD $(printf %q "$BASENAME")"
for a in "${EXTRA_ARGS[@]:-}"; do
    [ -z "$a" ] && continue
    REMOTE_CMD="$REMOTE_CMD $(printf %q "$a")"
done

echo "==> Launching marker-convert on remote (detached tmux)"
START_OUTPUT=$(ssh "$REMOTE_HOST" "$REMOTE_CMD")
echo "$START_OUTPUT"

REMOTE_SESSION="$(printf '%s\n' "$START_OUTPUT" | sed -n 's/^SESSION=//p' | head -1)"
REMOTE_LOG="$(printf '%s\n' "$START_OUTPUT" | sed -n 's/^LOG=//p' | head -1)"
REMOTE_OUTPUT="$(printf '%s\n' "$START_OUTPUT" | sed -n 's/^OUTPUT=//p' | head -1)"

if [ -z "$REMOTE_SESSION" ] || [ -z "$REMOTE_LOG" ] || [ -z "$REMOTE_OUTPUT" ]; then
    echo "Error: could not parse SESSION/LOG/OUTPUT from remote start output" >&2
    exit 1
fi

echo ""
echo "==> Polling $REMOTE_LOG every ${POLL_INTERVAL}s (timeout ${TIMEOUT}s)"
ELAPSED=0
FINAL_STATUS=""
while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
    sleep "$POLL_INTERVAL"
    ELAPSED=$(( ELAPSED + POLL_INTERVAL ))
    STATUS_LINE="$(ssh "$REMOTE_HOST" "grep -E 'STATUS: (DONE|FAILED)' $REMOTE_LOG 2>/dev/null | tail -1" || true)"
    if [ -n "$STATUS_LINE" ]; then
        FINAL_STATUS="$STATUS_LINE"
        break
    fi
    LAST_LINE="$(ssh "$REMOTE_HOST" "tail -1 $REMOTE_LOG 2>/dev/null" || true)"
    printf '  [%5ds] %s\n' "$ELAPSED" "${LAST_LINE:-(waiting...)}"
done

if [ -z "$FINAL_STATUS" ]; then
    echo "Error: timed out after ${TIMEOUT}s. Session $REMOTE_SESSION may still be running on $REMOTE_HOST." >&2
    echo "Inspect with: ssh $REMOTE_HOST 'tail -20 $REMOTE_LOG'" >&2
    exit 1
fi

echo ""
echo "==> Remote $FINAL_STATUS"

echo "==> Copying results back to $OUTPUT_DIR/$STEM"
rm -rf "$OUTPUT_DIR/$STEM"
scp -rq "$REMOTE_HOST:$REMOTE_OUTPUT" "$OUTPUT_DIR/"

if [ "$KEEP_REMOTE" = "0" ]; then
    echo "==> Cleaning up remote files"
    ssh "$REMOTE_HOST" "rm -rf $REMOTE_OUTPUT $REMOTE_DIR/$BASENAME"
fi

echo ""
echo "Done. Local output: $OUTPUT_DIR/$STEM"
ls -lh "$OUTPUT_DIR/$STEM" | head -20

if [[ "$FINAL_STATUS" == *FAILED* ]]; then
    exit 2
fi
