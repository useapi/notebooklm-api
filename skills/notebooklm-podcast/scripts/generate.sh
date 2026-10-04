#!/usr/bin/env bash
# Start an Audio Overview (podcast) or a Video Overview on a notebook and print the job id.
# Usage: generate.sh <notebook> audio|video [key=value ...]
#   audio: format=deep_dive|brief|critique|debate  length=short|default|long  language=en|es|pt_BR|...  instructions="..."
#   video: format=explainer|brief|cinematic|short  style=auto|classic|whiteboard|anime|...  language=...  instructions="..."
# The job runs on Google for minutes; poll it with wait-job.sh.
source "$(dirname "$0")/_common.sh"
NOTEBOOK="${1:?Usage: generate.sh <notebook> audio|video [key=value ...]}"
TYPE="${2:?Usage: generate.sh <notebook> audio|video [key=value ...]}"
shift 2

BODY=$(jq -n --arg nb "$NOTEBOOK" --arg type "$TYPE" '{notebook: $nb, type: $type, mode: "async"}')
for kv in "$@"; do
  BODY=$(jq --arg k "${kv%%=*}" --arg v "${kv#*=}" '.[$k] = $v' <<< "$BODY")
done
api POST artifacts "$BODY" | jq -r .jobid
