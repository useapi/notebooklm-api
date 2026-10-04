# Shared helpers for the notebooklm-podcast skill scripts. Sourced, not run.
# Needs: curl, jq. Env: USEAPI_TOKEN (required), USEAPI_EMAIL (optional, which connected Google account to use).
set -euo pipefail

API="${USEAPI_API:-https://api.useapi.net/v1/gemini-notebook}"
: "${USEAPI_TOKEN:?Set USEAPI_TOKEN to your useapi.net API token (https://useapi.net/docs/start-here/setup-useapi)}"
command -v jq > /dev/null || { echo "jq is required (https://jqlang.org/download/)" >&2; exit 1; }

AUTH=(-H "Authorization: Bearer $USEAPI_TOKEN")
enc() { jq -rn --arg v "$1" '$v|@uri'; }
log() { echo "$(date +%H:%M:%S) $*" >&2; }

# api METHOD PATH [JSON_BODY] -> response body on stdout; a non-2xx answer prints the error and exits 1
api() {
  local method="$1" path="$2" body="${3:-}" out code
  out=$(mktemp)
  if [ -n "$body" ]; then
    code=$(curl -sS --max-time 320 -o "$out" -w '%{http_code}' "${AUTH[@]}" -H "Content-Type: application/json" -X "$method" "$API/$path" -d "$body")
  else
    code=$(curl -sS --max-time 320 -o "$out" -w '%{http_code}' "${AUTH[@]}" -X "$method" "$API/$path")
  fi
  if [ "${code:0:1}" != "2" ]; then
    echo "$method /$path -> HTTP $code: $(cat "$out")" >&2
    rm -f "$out"
    exit 1
  fi
  cat "$out"
  rm -f "$out"
}
