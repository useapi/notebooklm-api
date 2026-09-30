#!/usr/bin/env bash
# USEAPI_TOKEN=user:12345-... EMAIL=user@example.com NOTEBOOK=<notebook id> CONVERSATION=<conversation id> NOTE=<note id> ./gemini-notebook-gallery.sh
set -euo pipefail

API="${API:-https://api.useapi.net/v1/gemini-notebook}"
: "${USEAPI_TOKEN:?export USEAPI_TOKEN=user:12345-...}"
: "${NOTEBOOK:?export NOTEBOOK=<notebook id>}"
OUT="gemini-notebook-gallery/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
mkdir -p "$OUT"
AUTH=(-H "Authorization: Bearer $USEAPI_TOKEN")
enc() { jq -rn --arg v "$1" '$v|@uri'; }
post() { curl -sS --max-time 310 "${AUTH[@]}" -H "Content-Type: application/json" -X POST "$API/$1" -d "$2"; }
get() { curl -sS "${AUTH[@]}" "$API/$1"; }
log() { echo "$(date +%H:%M:%S) $*"; }
wait_job() {
  until get "jobs/$(enc "$1")" > "$2" && jq -e '.status == "completed" or .status == "failed"' "$2" > /dev/null; do sleep 15; done
}
# A sync job that outlives the 90 s wait answers 202: poll it to the end
finish() {
  if jq -e '.status != "completed" and .status != "failed"' "$1" > /dev/null; then wait_job "$(jq -r .jobid "$1")" "$1"; fi
}

# 1. A follow-up question in the same conversation
if [ -n "${CONVERSATION:-}" ]; then
  post chat "$(jq -n --arg nb "$NOTEBOOK" --arg c "$CONVERSATION" '{notebook: $nb, conversation: $c, question: "How much fuel was left when they landed?"}')" > "$OUT/01-followup.json"
  jq -r '"follow-up: \(.answer[0:300])…\n  (\(.citations | length) citations)"' "$OUT/01-followup.json"
fi

# 2. The note from part 1 becomes a source
if [ -n "${NOTE:-}" ]; then
  post notes/source "$(jq -n --arg n "$NOTE" '{note: $n}')" > "$OUT/02-note-source.json"
  jq -r '"note → source: \(.kind) \(.status) \(.title)"' "$OUT/02-note-source.json"
fi

# 3. Quick Studio types, sync
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "flashcards", quantity: "fewer", difficulty: "easy"}')" > "$OUT/03-flashcards.json"
finish "$OUT/03-flashcards.json"
jq -r '"flashcards \(.status): \(.result.title), content keys \(.result.content | keys | join(","))\n  \(.result.content | tostring | .[0:240])…"' "$OUT/03-flashcards.json"

post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "mindmap"}')" > "$OUT/04-mindmap.json"
finish "$OUT/04-mindmap.json"
jq -r '"mind map \(.status): \(.result.title) (\(.result.content | tostring | length) bytes of JSON)"' "$OUT/04-mindmap.json"

post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "report", format: "briefing"}')" > "$OUT/05-report.json"
finish "$OUT/05-report.json"
jq -r '"report \(.status): \(.result.title) (\(.result.text | length) chars)"' "$OUT/05-report.json"

post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "table", instructions: "One row per program alarm or anomaly during the descent: time, alarm or event, cause, what the crew or Mission Control did."}')" > "$OUT/06-table.json"
finish "$OUT/06-table.json"
jq -r '"table \(.status): \(.result.title) (\(.result.table | length) rows incl. header)"' "$OUT/06-table.json"

# 4. A Video Overview and a slide deck, async
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "video", format: "explainer", style: "whiteboard", mode: "async"}')" > "$OUT/07-video-submit.json"
post artifacts "$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb, type: "slides", format: "presenter", length: "short", mode: "async"}')" > "$OUT/07-slides-submit.json"
for kind in slides video; do
  wait_job "$(jq -r .jobid "$OUT/07-$kind-submit.json")" "$OUT/08-$kind-job.json"
  log "$kind $(jq -r .status "$OUT/08-$kind-job.json"): $(jq -r '.result.title // .error.message' "$OUT/08-$kind-job.json")"
  jq -r '.result.files[]? | "\(.format) \(.url)"' "$OUT/08-$kind-job.json" | while read -r fmt url; do
    curl -sS "${AUTH[@]}" -o "$OUT/$kind.$fmt" "$url"
    log "  saved $OUT/$kind.$fmt ($(du -h "$OUT/$kind.$fmt" | cut -f1))"
  done
done
jq -r '.result.slides[0:2][] | .image' "$OUT/08-slides-job.json" | nl -v1 | while read -r n url; do
  curl -sS "${AUTH[@]}" -o "$OUT/slide-$n.png" "$url"
  log "  saved $OUT/slide-$n.png ($(du -h "$OUT/slide-$n.png" | cut -f1))"
done

# 5. Revise one slide with a prompt
post artifacts/revise "$(jq -n --arg a "$(jq -r .artifact "$OUT/08-slides-job.json")" '{artifact: $a, slide: 2, prompt: "Make this slide a simple timeline graphic.", mode: "async"}')" > "$OUT/09-revise-submit.json"
wait_job "$(jq -r .jobid "$OUT/09-revise-submit.json")" "$OUT/09-revise-job.json"
log "revise $(jq -r .status "$OUT/09-revise-job.json"): $(jq -r '.result.slides | length' "$OUT/09-revise-job.json") slides"
curl -sS "${AUTH[@]}" -o "$OUT/slide-2-revised.png" "$(jq -r '.result.slides[1].image' "$OUT/09-revise-job.json")"
log "  saved $OUT/slide-2-revised.png ($(du -h "$OUT/slide-2-revised.png" | cut -f1))"

if [ -n "${EMAIL:-}" ]; then get "accounts/$(enc "$EMAIL")" > "$OUT/10-account.json"; jq -r '"plan \(.googleTier): " + ([.quota.windows[] | "\(.window) used \(.usedPercent)%"] | join(", "))' "$OUT/10-account.json"; fi
log "all responses in $OUT"
