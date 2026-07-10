#!/bin/bash
# marker-convert.sh — Extract PDF on the marker GPU host (canonical copy).
#
# This file is the canonical version of the script. The Mac-side wrapper
# (pdf_to_md_via_gpu.sh) scp's it to the GPU host before each run, so
# any edits made here propagate automatically.
#
# Usage: ./marker-convert.sh [options] input.pdf [extra marker_single flags...]
#
# Options:
#   --human                 (default) Run in foreground; logs stream to terminal.
#   --ai                    Detached tmux session; prints session/log info, exits
#                           immediately. Caller polls $LOGFILE for "STATUS: DONE".
#   --formats fmt1,fmt2,... Comma-separated formats. Default: markdown.
#                           Valid: markdown, json, html. Each format = 1 marker pass.
#   --force-ocr             Pass --force_ocr to marker. Default OFF (PDFs with a
#                           clean text layer are faster + cleaner without it).
#   --help, -h              Show this help.
#
# Outputs: requested formats into ./<filename>/ relative to CWD.
# Log:     ./<filename>/marker-convert.log
#
# Monitor (--ai mode):
#   tmux has-session -t <session>   # 0 = running
#   tail -f ./<filename>/marker-convert.log
#   grep "STATUS: DONE" ./<filename>/marker-convert.log

set -euo pipefail

MODE="human"
FORMATS_CSV="markdown"
FORCE_OCR=0
POSITIONAL=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --human)      MODE="human"; shift ;;
        --ai)         MODE="ai"; shift ;;
        --formats)    FORMATS_CSV="$2"; shift 2 ;;
        --force-ocr)  FORCE_OCR=1; shift ;;
        --help|-h)
            awk 'NR>1 && /^#/{sub(/^# ?/,""); print; next} NR>1{exit}' "$0"
            exit 0
            ;;
        *)            POSITIONAL+=("$1"); shift ;;
    esac
done

set -- "${POSITIONAL[@]:-}"

if [ $# -lt 1 ] || [ -z "${1:-}" ]; then
    echo "Error: No input file specified. Run with --help for usage." >&2
    exit 1
fi

INPUT="$(realpath "$1")"
shift

if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT" >&2
    exit 1
fi

IFS=',' read -ra FORMATS <<< "$FORMATS_CSV"
for fmt in "${FORMATS[@]}"; do
    case "$fmt" in
        markdown|json|html) ;;
        *) echo "Error: unknown format '$fmt' (valid: markdown, json, html)" >&2; exit 1 ;;
    esac
done

BASENAME="$(basename "$INPUT")"
BASENAME="${BASENAME%.pdf}"
BASENAME="${BASENAME%.PDF}"
OUTPUT_DIR="$(pwd)/$BASENAME"
LOGFILE="$OUTPUT_DIR/marker-convert.log"
SESSION_NAME="${BASENAME//[^a-zA-Z0-9_-]/_}"

mkdir -p "$OUTPUT_DIR"

EXTRA_ARGS=""
for arg in "$@"; do
    EXTRA_ARGS="$EXTRA_ARGS $(printf '%q' "$arg")"
done

FORMATS_JOINED="$(IFS=' '; echo "${FORMATS[*]}")"

WORKER_SCRIPT=$(cat <<'WORKER_EOF'
#!/bin/bash
set -euo pipefail

INPUT="__INPUT__"
OUTPUT_DIR="__OUTPUT_DIR__"
LOGFILE="__LOGFILE__"
FORCE_OCR=__FORCE_OCR__
FORMATS=(__FORMATS__)
EXTRA_ARGS=(__EXTRA_ARGS__)

source ~/.myenv/bin/activate

# Pass the PARENT directory to marker. marker_single creates a subdir
# inside --output_dir named after the input PDF basename, so this yields
# $OUTPUT_DIR (= parent/$BASENAME) containing the actual output files.
COMMON_FLAGS=(
    --output_dir "$(dirname "$OUTPUT_DIR")"
    --highres_image_dpi 288
    --paginate_output
)
if [ "$FORCE_OCR" = "1" ]; then
    COMMON_FLAGS+=(--force_ocr)
fi

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

{
    log "========================================"
    log "marker-convert starting"
    log "Input:       $INPUT"
    log "Output:      $OUTPUT_DIR"
    log "Formats:     ${FORMATS[*]}"
    log "force_ocr:   $FORCE_OCR"
    log "Extra flags: ${EXTRA_ARGS[*]:-none}"
    log "========================================"

    OVERALL_START=$SECONDS
    FAILED=0

    for fmt in "${FORMATS[@]}"; do
        log "--- Starting pass: $fmt ---"
        PASS_START=$SECONDS

        if marker_single "$INPUT" \
            "${COMMON_FLAGS[@]}" \
            --output_format "$fmt" \
            "${EXTRA_ARGS[@]}"; then
            log "--- Completed pass: $fmt ($(( SECONDS - PASS_START ))s) ---"
        else
            log "--- FAILED pass: $fmt ($(( SECONDS - PASS_START ))s) ---"
            FAILED=1
        fi
    done

    log "========================================"
    log "All passes complete. Total time: $(( SECONDS - OVERALL_START ))s"
    log "Output directory: $OUTPUT_DIR"
    log "Contents:"
    ls -lh "$OUTPUT_DIR"/
    log "========================================"
    if [ "$FAILED" = "1" ]; then
        log "STATUS: FAILED"
    else
        log "STATUS: DONE"
    fi
} 2>&1 | tee -a "$LOGFILE"
WORKER_EOF
)

WORKER_SCRIPT="${WORKER_SCRIPT//__INPUT__/$INPUT}"
WORKER_SCRIPT="${WORKER_SCRIPT//__OUTPUT_DIR__/$OUTPUT_DIR}"
WORKER_SCRIPT="${WORKER_SCRIPT//__LOGFILE__/$LOGFILE}"
WORKER_SCRIPT="${WORKER_SCRIPT//__FORCE_OCR__/$FORCE_OCR}"
WORKER_SCRIPT="${WORKER_SCRIPT//__FORMATS__/$FORMATS_JOINED}"
WORKER_SCRIPT="${WORKER_SCRIPT//__EXTRA_ARGS__/$EXTRA_ARGS}"

WORKER_FILE="$OUTPUT_DIR/.marker-worker.sh"
printf '%s\n' "$WORKER_SCRIPT" > "$WORKER_FILE"
chmod +x "$WORKER_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Session: $SESSION_NAME" > "$LOGFILE"

if [ "$MODE" = "ai" ]; then
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
    # Quote the worker path: tmux runs this as a shell command string, so an
    # unquoted path containing spaces would make tmux run `bash <first-word>`
    # and the session would die instantly with no error in the log. printf %q
    # produces a shell-safe token for any path.
    tmux new-session -d -s "$SESSION_NAME" "bash $(printf %q "$WORKER_FILE")"

    cat <<EOF
MARKER-CONVERT STARTED
======================
SESSION=$SESSION_NAME
LOG=$LOGFILE
OUTPUT=$OUTPUT_DIR
FORMATS=${FORMATS[*]}
FORCE_OCR=$FORCE_OCR

COMMANDS:
  Check if running:    tmux has-session -t $SESSION_NAME 2>/dev/null && echo running || echo done
  View live progress:  tmux attach -t $SESSION_NAME
  Tail the log:        tail -20 $LOGFILE
  Check completion:    grep -E 'STATUS: (DONE|FAILED)' $LOGFILE
  List output files:   ls -lh $OUTPUT_DIR/
======================
EOF
else
    echo "Converting: $INPUT"
    echo "Output:     $OUTPUT_DIR"
    echo "Log:        $LOGFILE"
    echo "Formats:    ${FORMATS[*]}"
    echo "force_ocr:  $FORCE_OCR"
    echo ""
    bash "$WORKER_FILE"
fi
