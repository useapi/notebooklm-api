#!/usr/bin/env bash
# Download every file of a finished job (an .m4a for audio, an .mp4 for video) and print the saved paths.
# Usage: download.sh <job.json|-> [OUT_DIR]
# The download links need the same API token, so they cannot be opened in a browser as they are.
source "$(dirname "$0")/_common.sh"
JOB=$(cat "${1:--}")
OUT="${2:-.}"
mkdir -p "$OUT"

NAME=$(jq -r '.result.title // "notebooklm"' <<< "$JOB" | tr -cs 'A-Za-z0-9_-' '_' | cut -c1-60 | sed 's/_$//')
jq -r '.result.files[] | "\(.format)\t\(.url)"' <<< "$JOB" | while IFS=$'\t' read -r FORMAT URL; do
  FILE="$OUT/$NAME.$FORMAT"
  curl -sS --fail --max-time 600 "${AUTH[@]}" -o "$FILE" "$URL"
  echo "$FILE"
done
