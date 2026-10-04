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

NOTEBOOK=$(bash "$DIR/create-notebook.sh" "$TITLE")
log "notebook $NOTEBOOK"
if [ ${#URLS[@]} -gt 0 ]; then bash "$DIR/add-sources.sh" "$NOTEBOOK" "${URLS[@]}" >&2; fi
if [ ${#FILES[@]} -gt 0 ]; then
  for f in "${FILES[@]}"; do bash "$DIR/upload-file.sh" "$NOTEBOOK" "$f" >&2; done
fi
bash "$DIR/wait-sources.sh" "$NOTEBOOK" >&2
# generate.sh logs the job id (and how to resume with it) on stderr
JOBID=$(bash "$DIR/generate.sh" "$NOTEBOOK" audio ${OPTS[@]+"${OPTS[@]}"})
JOB_FILE=$(mktemp)
trap 'rm -f "$JOB_FILE"' EXIT
bash "$DIR/wait-job.sh" "$JOBID" > "$JOB_FILE"
jq -r '"\"\(.result.title)\", \(.result.duration) s"' "$JOB_FILE" >&2
bash "$DIR/download.sh" "$JOB_FILE" "${OUT_DIR:-.}"
