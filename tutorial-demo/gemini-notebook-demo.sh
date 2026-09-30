#!/usr/bin/env bash
# USEAPI_TOKEN=user:12345-... EMAIL=user@example.com ./gemini-notebook-demo.sh [path/to/file.pdf]
set -euo pipefail

API="${API:-https://api.useapi.net/v1/gemini-notebook}"
: "${USEAPI_TOKEN:?export USEAPI_TOKEN=user:12345-...}"
: "${EMAIL:?export EMAIL=<your connected Google account>}"
PDF="${1:-}"
OUT="gemini-notebook-demo/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT"
AUTH=(-H "Authorization: Bearer $USEAPI_TOKEN")
enc() { jq -rn --arg v "$1" '$v|@uri'; }
# Research import can take a minute or two (Google fetches every URL first); the API answers within about 2 minutes
post() { curl -sS --max-time 310 "${AUTH[@]}" -H "Content-Type: application/json" -X POST "$API/$1" -d "$2"; }
get() { curl -sS "${AUTH[@]}" "$API/$1"; }
log() { echo "$(date +%H:%M:%S) $*"; }
wait_job() {
  until get "jobs/$(enc "$1")" > "$2" && jq -e '.status == "completed" or .status == "failed"' "$2" > /dev/null; do sleep 15; done
}

# 1. A notebook on your account
post notebooks "$(jq -n --arg email "$EMAIL" '{email: $email, title: "Apollo 11"}')" > "$OUT/01-notebook.json"
NOTEBOOK=$(jq -r .notebook "$OUT/01-notebook.json")
log "notebook $NOTEBOOK"

# 2. Sources: a web page, a YouTube video and pasted text in one call
post sources "$(jq -n --arg nb "$NOTEBOOK" '{
  notebook: $nb,
  urls: ["https://en.wikipedia.org/wiki/Apollo_11", "https://www.youtube.com/watch?v=xUcYQ7slmRw"],
  title: "Why Apollo 11 almost did not land",
  text: "During the descent the guidance computer raised 1202 and 1201 program alarms, and Armstrong flew the final approach manually to avoid a boulder field, landing with little fuel to spare."
}')" > "$OUT/02-sources.json"
jq -r '.sources[] | "  \(.kind) \(.status) \(.title)"' "$OUT/02-sources.json"

# 3. Optional: a file, sent as the raw request body
if [ -n "$PDF" ]; then
  curl -sS "${AUTH[@]}" -H "Content-Type: application/pdf" --data-binary "@$PDF" \
    "$API/sources/upload?notebook=$(enc "$NOTEBOOK")&name=$(enc "$(basename "$PDF")")" > "$OUT/03-upload.json"
  log "uploaded $(jq -r .title "$OUT/03-upload.json") ($(jq -r .status "$OUT/03-upload.json"))"
fi

# 4. Wait until Google has processed every source
until get "notebooks/$(enc "$NOTEBOOK")" > "$OUT/04-notebook.json" &&
      jq -e '[.sources[].status] | all(. == "ready" or . == "error")' "$OUT/04-notebook.json" > /dev/null; do
  log "sources: $(jq -r '[.sources[].status] | join(",")' "$OUT/04-notebook.json")"
  sleep 10
done
log "sources ready: $(jq -r '[.sources[] | .kind] | join(", ")' "$OUT/04-notebook.json")"

# 5. What one source is about: Google's summary and key topics
WEB=$(jq -r '.sources[] | select(.kind == "web") | .source' "$OUT/04-notebook.json" | head -1)
get "sources/$(enc "$WEB")" > "$OUT/05-source.json"
jq -r '"guide: \(.summary[0:200])…\n  topics: \(.topics | join(", "))"' "$OUT/05-source.json"

# 6. Ask the notebook a question (answer + numbered citations)
post chat "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, question: "What went wrong during the descent, and how did the crew handle it?"}')" > "$OUT/06-chat.json"
jq -r '"\(.answer[0:400])…\n  (\(.citations | length) citations, \(.ms) ms)"' "$OUT/06-chat.json"

# 7. Keep the answer as a note
post notes "$(jq -n --arg nb "$NOTEBOOK" --arg a "$(jq -r .answer "$OUT/06-chat.json")" '{notebook: $nb, title: "What went wrong during the descent", content: $a}')" > "$OUT/07-note.json"
log "note $(jq -r .title "$OUT/07-note.json") ($(jq -r '.content | length' "$OUT/07-note.json") chars)"

# 8. Find more sources on the web (Discover, sync) and import three of them
post research "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "fast", query: "Apollo 11 lunar module guidance computer alarms"}')" > "$OUT/08-discover.json"
jq -r '"discover \(.status): \(.result.sources | length) sources: \(.result.summary)"' "$OUT/08-discover.json"
post research/import "$(jq -n --arg j "$(jq -r .jobid "$OUT/08-discover.json")" --argjson urls "$(jq '[.result.sources[0:3][].url]' "$OUT/08-discover.json")" '{jobid: $j, urls: $urls}')" > "$OUT/08-discover-import.json"
jq -r '.sources[] | "  imported \(.kind) \(.status) \(.title)"' "$OUT/08-discover-import.json"

# 9. Deep Research runs for minutes: start it async now, collect it at the end
post research "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "deep", query: "Why did the Apollo 11 landing nearly abort?", mode: "async"}')" > "$OUT/09-deep-submit.json"
log "deep research $(jq -r .status "$OUT/09-deep-submit.json")"

# 10. A quiz, sync: the answer is the finished job
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "quiz", quantity: "fewer", difficulty: "medium"}')" > "$OUT/10-quiz.json"
jq -r '"quiz \(.status): \(.result.content.quiz | length) questions, first: \(.result.content.quiz[0].question)"' "$OUT/10-quiz.json"

# 11. An Audio Overview and an infographic, async: submit both, then poll
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "audio", format: "brief", length: "short", mode: "async"}')" > "$OUT/11-audio-submit.json"
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "infographic", orientation: "portrait", style: "sketch_note", mode: "async"}')" > "$OUT/11-infographic-submit.json"
for kind in audio infographic; do
  wait_job "$(jq -r .jobid "$OUT/11-$kind-submit.json")" "$OUT/12-$kind-job.json"
  log "$kind $(jq -r .status "$OUT/12-$kind-job.json"): $(jq -r '.result.title // .error.message' "$OUT/12-$kind-job.json")"
  # Files come through GET /artifacts/download, with your API token
  jq -r '.result.files[]? | "\(.format) \(.url)"' "$OUT/12-$kind-job.json" | while read -r fmt url; do
    curl -sS "${AUTH[@]}" -o "$OUT/$kind.$fmt" "$url"
    log "  saved $OUT/$kind.$fmt ($(du -h "$OUT/$kind.$fmt" | cut -f1))"
  done
done

# 12. The Deep Research result, then its report imported as a source
wait_job "$(jq -r .jobid "$OUT/09-deep-submit.json")" "$OUT/13-deep-job.json"
jq -r '"deep research \(.status): \"\(.result.report.title)\" (\(.result.report.markdown | length) chars), \(.result.sources | length) sources, \([.result.sources[] | select(.cited)] | length) cited"' "$OUT/13-deep-job.json"
post research/import "$(jq -n --arg j "$(jq -r .jobid "$OUT/13-deep-job.json")" '{jobid: $j, urls: [], report: true}')" > "$OUT/13-deep-import.json"
jq -r '.sources[] | "  imported \(.kind) \(.status) \(.title)"' "$OUT/13-deep-import.json"

# 13. Share the notebook: anyone with the link can view it, without copying it
post sharing "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, link: "public", allowCopies: false}')" > "$OUT/14-sharing.json"
jq -r '"sharing: link \(.link), copies \(.allowCopies), people: \([.people[] | "\(.email) (\(.role))"] | join(", "))"' "$OUT/14-sharing.json"

# 14. What that cost against Google's usage windows
get "accounts/$(enc "$EMAIL")" > "$OUT/15-account.json"
jq -r '"plan \(.googleTier): " + ([.quota.windows[] | "\(.window) used \(.usedPercent)%"] | join(", "))' "$OUT/15-account.json"
log "all responses in $OUT"
