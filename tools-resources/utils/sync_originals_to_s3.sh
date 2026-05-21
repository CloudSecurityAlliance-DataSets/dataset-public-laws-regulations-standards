#!/usr/bin/env bash
# Mirror binary originals (PDF / XLSX / DOCX / ZIP) at SecID-canonical paths
# into s3://dataset-public-laws-regulations-standards/<relative-path>.
#
# Idempotent: aws s3 sync only uploads files that don't already exist (or have
# different size/etag). Safe to re-run after new docs land.
#
# Usage:
#   tools-resources/utils/sync_originals_to_s3.sh           # do it
#   tools-resources/utils/sync_originals_to_s3.sh --dry-run # preview
#
# Notes:
# - Operates on the four SecID type roots only (control/ regulation/ reference/
#   methodology/). Other roots (weakness/ ttp/) currently have no binary
#   originals; loop iterates them in case future originals appear.
# - Skips tools-resources/PROCESSED-US/ DOCX (not at SecID-canonical paths;
#   needs manual mapping per doc — handled separately).
# - Marker output artifacts (_page_*.jpeg, *_meta.json, *.md, *.json) are NOT
#   uploaded by this script. S3 archives originals only; extractions live in
#   git and are re-derivable from the originals + the extractor scripts.
# - Profile: csa (assumes ~/.aws/config has the csa profile).
set -euo pipefail

BUCKET="s3://dataset-public-laws-regulations-standards"
PROFILE="csa"
TYPE_ROOTS=(control regulation reference methodology weakness ttp capability advisory disclosure entity)

DRY_RUN=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN="--dryrun" ;;
        --help|-h)
            sed -n '2,/^$/p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *) echo "Unknown flag: $arg" >&2; exit 2 ;;
    esac
done

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

uploaded_any=0
for root in "${TYPE_ROOTS[@]}"; do
    [ -d "$root" ] || continue
    echo "==> Syncing $root/ to $BUCKET/$root/"
    aws --profile "$PROFILE" s3 sync "$root/" "$BUCKET/$root/" \
        $DRY_RUN \
        --exclude "*" \
        --include "*.pdf" \
        --include "*.xlsx" \
        --include "*.xls" \
        --include "*.docx" \
        --include "*.zip" \
        --include "*.tar.gz"
    uploaded_any=1
done

if [ "$uploaded_any" = 0 ]; then
    echo "No type-root directories found under $REPO_ROOT" >&2
    exit 1
fi

echo
echo "Done. To verify what's in S3:"
echo "  aws --profile $PROFILE s3 ls --recursive --human-readable --summarize $BUCKET/"
