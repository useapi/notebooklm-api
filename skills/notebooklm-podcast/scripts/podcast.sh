#!/usr/bin/env bash
# One command: links (and optional local files) -> a NotebookLM Audio Overview saved as .m4a.
# Usage: podcast.sh "<title>" URL|FILE [URL|FILE ...] [-- key=value ...]
# Example: podcast.sh "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=brief length=short
# Arguments that are existing local files are uploaded; everything else is added as a URL.
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
TITLE="${1:?Usage: podcast.sh \"<title>\" URL|FILE ... [-- key=value ...]}"
shift
URLS=() FILES=() OPTS=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--" ]; then shift; OPTS=("$@"); break; fi
  if [ -f "$1" ]; then FILES+=("$1"); else URLS+=("$1"); fi
  shift
done

NOTEBOOK=$("$DIR/create-notebook.sh" "$TITLE")
log "notebook $NOTEBOOK"
if [ ${#URLS[@]} -gt 0 ]; then "$DIR/add-sources.sh" "$NOTEBOOK" "${URLS[@]}" >&2; fi
for f in "${FILES[@]}"; do "$DIR/upload-file.sh" "$NOTEBOOK" "$f" >&2; done
"$DIR/wait-sources.sh" "$NOTEBOOK" >&2
JOBID=$("$DIR/generate.sh" "$NOTEBOOK" audio "${OPTS[@]}")
log "audio job $JOBID"
JOB_FILE=$(mktemp)
"$DIR/wait-job.sh" "$JOBID" > "$JOB_FILE"
jq -r '"\"\(.result.title)\", \(.result.duration) s"' "$JOB_FILE" >&2
"$DIR/download.sh" "$JOB_FILE" "${OUT_DIR:-.}"
rm -f "$JOB_FILE"
