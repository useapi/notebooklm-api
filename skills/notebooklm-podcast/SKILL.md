---
name: notebooklm-podcast
description: Turn web pages, YouTube videos, pasted text or local files (PDF, Word, EPUB, audio...) into a NotebookLM Audio Overview podcast (.m4a) or a Video Overview (.mp4) through the useapi.net Gemini Notebook API (NotebookLM was renamed Gemini Notebook). Use when the user asks to make a NotebookLM podcast or audio overview, turn articles or documents into a podcast, generate a NotebookLM video overview, or automate NotebookLM / Gemini Notebook from the command line. Needs curl, jq and a USEAPI_TOKEN environment variable.
license: MIT
compatibility: Needs bash, curl, jq and network access to api.useapi.net. Requires a useapi.net API token (USEAPI_TOKEN) and a Google account connected to useapi.net.
metadata:
  author: useapi.net
  homepage: https://github.com/useapi/notebooklm-api
---

# NotebookLM podcast (Audio Overview) with the Gemini Notebook API

These scripts call the [useapi.net Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1), a third-party REST API that drives the user's own Google NotebookLM (Gemini Notebook) account. Every script is in `scripts/` next to this file. Run them with bash.

## Before you start

1. `USEAPI_TOKEN` must be set. If it is missing, ask the user for their useapi.net API token (setup: https://useapi.net/docs/start-here/setup-useapi) and their Google account must already be connected (https://useapi.net/docs/start-here/setup-gemini-notebook). Never print the token or write it to a file.
2. `USEAPI_EMAIL` is optional: the connected Google account to run on. Leave it unset and the API picks a healthy account with usage left.
3. `curl` and `jq` must be installed.

## Fastest path: one command

```bash
scripts/podcast.sh "<title>" <URL or local file> [more ...] [-- key=value ...]
```

Example:

```bash
scripts/podcast.sh "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=brief length=short
```

Arguments that are existing local files are uploaded, everything else is added as a URL. It prints progress on stderr and the saved `.m4a` path on stdout (`OUT_DIR` sets the folder, default the current one). A short brief takes about 3 to 10 minutes. Tell the user it is running and wait for it; do not start a second copy.

## Step by step (for video, pasted text, or more control)

1. Create a notebook. It prints the notebook id; keep it.
   ```bash
   NB=$(scripts/create-notebook.sh "My topic")
   ```
2. Add sources. URLs (web pages and YouTube, up to 50 per call) and pasted text:
   ```bash
   scripts/add-sources.sh "$NB" https://example.com/article https://www.youtube.com/watch?v=VIDEO_ID
   scripts/add-sources.sh "$NB" --text notes.txt --title "My notes"      # or --text - to read stdin
   ```
   Local files (PDF, DOCX, PPTX, EPUB, MD, TXT, CSV, MP3, M4A, WAV, MP4, JPG, PNG; up to 200 MB):
   ```bash
   scripts/upload-file.sh "$NB" ./report.pdf
   ```
3. Wait until Google has processed every source (polls every 10 s). A YouTube video without captions ends as `error` and is skipped.
   ```bash
   scripts/wait-sources.sh "$NB"
   ```
4. Start the generation. It prints the job id.
   ```bash
   JOB=$(scripts/generate.sh "$NB" audio format=deep_dive length=default language=en)
   JOB=$(scripts/generate.sh "$NB" video format=explainer style=whiteboard)
   ```
5. Wait for the job (polls every 15 s) and save the final record:
   ```bash
   scripts/wait-job.sh "$JOB" > job.json
   ```
6. Download the file(s). Prints the saved paths:
   ```bash
   scripts/download.sh job.json ./out
   ```

## Options

| `type` | `format` | Other options |
|---|---|---|
| `audio` | `deep_dive` (default), `brief`, `critique`, `debate` | `length`: `short`, `default`, `long`; `language` (e.g. `en`, `es`, `pt_BR`, `zh_Hans`); `instructions` |
| `video` | `explainer` (default), `brief`, `cinematic`, `short` | `style`: `auto`, `classic`, `whiteboard`, `heritage`, `paper_craft`, `watercolor`, `anime`, `retro_print`, `kawaii`; `language`, `instructions` (not with `cinematic`; `short` takes no `style`) |

Pass options as `key=value` to `generate.sh` (or after `--` to `podcast.sh`), e.g. `instructions="Focus on the risks"`. Any other option returns `400` with the valid values. Full list: https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts

## Errors

- `HTTP 401`: the token is wrong. `HTTP 404` from `create-notebook.sh`: `USEAPI_EMAIL` is not a connected account.
- `HTTP 596`: the Google account needs to be reconnected (or, without `USEAPI_EMAIL`, no healthy account is left). Point the user to https://useapi.net/docs/start-here/setup-gemini-notebook.
- `HTTP 429`: every account is busy or out of NotebookLM usage. The body carries `retryAt` when Google names the reset time. Tell the user when they can retry, or set `USEAPI_EMAIL` to another connected account. Do not loop on it.
- `HTTP 409` from `generate.sh`: no source is `ready` yet. Run `wait-sources.sh` first.
- A failed job prints its `error`. A job still running after 40 minutes is failed by the API with `timeout`.

## After it finishes

Tell the user the file path, the episode title and its duration (`result.title` and `result.duration` in `job.json`). The notebook stays in their NotebookLM account, so they can open it there or generate more from it with `generate.sh "$NB" ...`.
