# NotebookLM (Gemini Notebook) by useapi.net

**Author:** [useapi](https://useapi.net/?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin) · **Version:** 0.1.1 · **Type:** tool · **Source:** https://github.com/useapi/notebooklm-api/tree/main/dify-plugin · **Contact:** support@useapi.net

Use Google Gemini Notebook, formerly NotebookLM, from Dify [workflows, chatflows](https://docs.dify.ai/en/cloud/use-dify/build/workflow-chatflow) and [agents](https://docs.dify.ai/en/cloud/use-dify/build/new-agent/overview). Create notebooks, add web pages, YouTube videos, text, Google Drive files and uploads as sources, ask questions answered with citations, run Deep Research, and generate every Studio output: Audio Overviews (the Gemini Notebook podcast), Video Overviews, slide decks, infographics, reports, data tables, quizzes, flashcards and mind maps. Audio, video, slides and images come back as Dify files.

> This plugin calls the [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin) by useapi.net, a third-party API. It is not made by, affiliated with or endorsed by Google. It needs a useapi.net subscription ($15/month, covers every useapi.net API) and a Google account. Generation runs on that account's Google AI subscription, the free plan included, with no per-call charge from useapi.net.

Google offers no Gemini Notebook API for regular Google accounts; its only one, the Gemini Notebook Enterprise API, needs Enterprise licenses in a Google Cloud project. This plugin works with a regular Google account.

## Setup

1. **Get a useapi.net API token.** Subscribe and copy your token: [Setup useapi.net](https://useapi.net/docs/start-here/setup-useapi?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin).
2. **Connect your Google account once.** Follow [Setup Gemini Notebook](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin): you sign in with Google, with no cookies to copy and no Google Cloud project. Each subscription covers 3 Google accounts (up to 100), and new jobs are spread across them.
3. **Install the plugin** from the [Dify Marketplace](https://marketplace.dify.ai/plugins/useapi/notebooklm_useapi), or upload the `.difypkg` from the [GitHub releases](https://github.com/useapi/notebooklm-api/releases) under Plugins > Install plugin > Local package file.
4. **Authorize it.** In Tools, open "NotebookLM (Gemini Notebook) by useapi.net", click Authorize and fill in:

| Credential | Required | What it is |
|---|:-:|---|
| `useapi.net API token` | Yes | Your token from step 1. Stored by Dify as a secret. |
| `Default Google account email` | No | Which connected Google account to use when a tool needs one. Leave empty to let useapi.net pick the least busy healthy account. |

Saving the credentials makes one cheap check, `GET /accounts`, which confirms the token works and that at least one Google account is connected.

### Connection requirements

The plugin connects only to `https://api.useapi.net/v1/gemini-notebook` over HTTPS, with the token in an `Authorization: Bearer` header. A self-hosted Dify needs outbound HTTPS to `api.useapi.net`. No proxy, webhook or inbound connection is required.

## Tools

56 tools, one per task, with the API's own options as dropdowns. Ids look like `user:12345-you@example.com-notebook:<uuid>`; pass them between nodes as variables.

### Studio outputs (generation)

Every generation tool takes either a `notebook` id, or `urls` and/or `text` to create a notebook on the fly (one-shot). They wait up to 120 seconds by default, then return the result text, the files and workflow variables. If the job is still running, they return a message with its `jobid`; call **Get job status** with that `jobid` (it also waits up to 120 seconds per call) until the result arrives. This keeps every agent turn short. In a workflow, raise "Maximum wait" (up to 540 seconds) to get the file in one node.

| Tool | What you get | Options |
|---|---|---|
| `generate_audio_overview` | Podcast `.m4a` | format `deep_dive`, `brief`, `critique`, `debate`; length `short`, `default`, `long`; language; instructions |
| `generate_video_overview` | Video `.mp4` | format `explainer`, `brief`, `cinematic`, `short`; style `auto`, `classic`, `whiteboard`, `heritage`, `paper_craft`, `watercolor`, `anime`, `retro_print`, `kawaii`, `custom` with a style prompt; language; instructions |
| `generate_slide_deck` | `.pdf` and `.pptx`, slide text | format `detailed`, `presenter`; length; language; instructions |
| `generate_infographic` | `.png` and text | 11 styles; orientation `landscape`, `portrait`, `square`; detail `concise`, `standard`, `detailed` |
| `generate_report` | Markdown | format `briefing`, `study_guide`, `blog_post`, `custom` (instructions become the prompt) |
| `generate_interactive_report` | Text and suggested items | language; instructions |
| `generate_data_table` | Markdown table and rows | language; instructions (which columns) |
| `generate_quiz` | Questions with marked answers, and JSON | quantity `fewer`, `standard`, `more`; difficulty `easy`, `medium`, `hard` |
| `generate_flashcards` | Cards and JSON | quantity; difficulty |
| `generate_mind_map` | Outline and JSON tree | instructions |
| `generate_suggested_item` | An item an interactive report suggested | per-type options |
| `retry_artifact` | Re-runs a failed generation | |
| `revise_slide` | Changes one slide of a deck with a prompt | slide number, prompt |

### All tools and their endpoints

Endpoints are relative to `https://api.useapi.net/v1/gemini-notebook`.

| Tool | Label | Endpoint |
|---|---|---|
| `list_accounts` | List Google accounts | `GET /accounts` |
| `get_account` | Get account usage | `GET /accounts/{email}` |
| `list_jobs` | List running jobs | `GET /jobs` |
| `get_job` | Get job status | `GET /jobs/{jobid}` |
| `cancel_job` | Cancel job | `DELETE /jobs/{jobid}` |
| `list_notebooks` | List notebooks | `GET /notebooks` |
| `create_notebook` | Create notebook | `POST /notebooks` |
| `get_notebook` | Get notebook | `GET /notebooks/{notebook}` |
| `rename_notebook` | Rename notebook | `POST /notebooks/{notebook}` |
| `delete_notebook` | Delete notebook | `DELETE /notebooks/{notebook}` |
| `copy_notebook` | Copy notebook | `POST /notebooks/copy` |
| `get_notebook_guide` | Get notebook guide | `GET /notebooks/guide` |
| `get_sharing` | Get sharing settings | `GET /sharing` |
| `share_notebook` | Share notebook | `POST /sharing` |
| `add_sources` | Add sources | `POST /sources` |
| `upload_source` | Upload file as source | `POST /sources/upload` |
| `get_source` | Get source | `GET /sources/{source}` |
| `rename_source` | Rename source | `POST /sources/{source}` |
| `delete_source` | Delete source | `DELETE /sources/{source}` |
| `sync_drive_source` | Sync Google Drive source | `POST /sources/sync` |
| `append_to_source` | Append text to source | `POST /sources/append` |
| `search_sources` | Search sources | `POST /sources/search` |
| `list_play_books` | List Play Books | `GET /sources/books` |
| `ask_notebook` | Ask notebook (cited chat) | `POST /chat` |
| `get_chat_history` | Get chat history | `GET /chat` |
| `clear_chat` | Clear chat | `DELETE /chat` |
| `configure_chat` | Configure chat | `POST /chat/settings` |
| `research` | Research (Discover sources / Deep Research) | `POST /research` |
| `import_research` | Import research results | `POST /research/import` |
| `generate_audio_overview` | Generate Audio Overview (podcast) | `POST /artifacts` (type `audio`) |
| `generate_video_overview` | Generate Video Overview | `POST /artifacts` (type `video`) |
| `generate_slide_deck` | Generate slide deck | `POST /artifacts` (type `slides`) |
| `generate_infographic` | Generate infographic | `POST /artifacts` (type `infographic`) |
| `generate_report` | Generate report | `POST /artifacts` (type `report`) |
| `generate_interactive_report` | Generate interactive report | `POST /artifacts` (type `interactive_report`) |
| `generate_data_table` | Generate data table | `POST /artifacts` (type `table`) |
| `generate_quiz` | Generate quiz | `POST /artifacts` (type `quiz`) |
| `generate_flashcards` | Generate flashcards | `POST /artifacts` (type `flashcards`) |
| `generate_mind_map` | Generate mind map | `POST /artifacts` (type `mindmap`) |
| `generate_suggested_item` | Generate a suggested item | `POST /artifacts/generate` |
| `retry_artifact` | Retry failed artifact | `POST /artifacts/retry` |
| `revise_slide` | Revise a slide | `POST /artifacts/revise` |
| `list_artifacts` | List artifacts | `GET /artifacts` |
| `get_artifact` | Get artifact | `GET /artifacts/{artifact}` |
| `download_artifact` | Download artifact file | `GET /artifacts/download` |
| `delete_artifact` | Delete artifact | `DELETE /artifacts/{artifact}` |
| `export_artifact` | Export to Google Docs or Sheets | `POST /artifacts/export` |
| `list_notes` | List notes | `GET /notes` |
| `create_note` | Create note | `POST /notes` |
| `delete_note` | Delete note | `DELETE /notes/{note}` |
| `note_to_source` | Convert note to source | `POST /notes/source` |
| `list_labels` | List source labels | `GET /labels` |
| `create_labels` | Label sources | `POST /labels` |
| `list_collections` | List collections | `GET /collections` |
| `create_collection` | Create collection | `POST /collections` |
| `update_collection` | Update collection | `POST /collections/{collection}` |

### Outputs

Each tool returns three kinds of output:

- **text**: a readable summary, an answer with its citations, or the rendered result (a report, a Markdown table, a quiz with the correct answers marked, a mind map outline, a Deep Research report with its sources). This is what an agent reads.
- **json**: the full API response.
- **files**: for audio, video, slides and infographics, the `.m4a`, `.mp4`, `.pdf`, `.pptx` or `.png` itself (turn off "Attach the file" to skip it). Files over 150 MB are not attached; download them with your token from `file_urls`.

Tools also set **variables** you can reference in later nodes without a Code node, for example `notebook` from Create notebook, `source_ids` and `ready` from Add sources, `answer` and `conversation` from Ask notebook, and `jobid`, `status`, `notebook`, `artifact`, `title`, `text` and `file_urls` from every generation tool.

## Usage examples

### Workflow: links to podcast in one node

```
[Start: urls (paragraph)]
        |
[NotebookLM > Generate Audio Overview (podcast)]
    urls     = {{Start.urls}}
    format   = Deep dive        length = Short
    language = en               Wait for the result = on, Maximum wait = 540
        |
[End: podcast = {{Generate Audio Overview.files}},
      summary = {{Generate Audio Overview.text}}]
```

No notebook is needed: the tool creates one for these links, waits for the sources, generates the Audio Overview and returns the `.m4a` file. A short Audio Overview usually takes 3 to 6 minutes, so set Maximum wait to 540 here; if it is still running then, add a Get job status node with `jobid = {{Generate Audio Overview.jobid}}`.

### Workflow: research a topic, then ask and present

```
[Start: topic]
  -> [Create notebook]            title    = {{Start.topic}}
  -> [Research]                   notebook = {{Create notebook.notebook}}
                                  query    = {{Start.topic}}   type = Deep Research
  -> [Import research results]    jobid    = {{Research.jobid}}
  -> [Ask notebook]               notebook = {{Create notebook.notebook}}
                                  question = "What are the three key findings?"
  -> [Generate slide deck]        notebook = {{Create notebook.notebook}}
  -> [End: answer = {{Ask notebook.answer}}, slides = {{Generate slide deck.files}}]
```

### Agent: a research assistant over your notebooks

Create an Agent app, add the tools List notebooks, Get notebook, Add sources, Ask notebook, Generate Audio Overview and Get job status, and use instructions like:

```
You help the user work with their Gemini Notebook (NotebookLM) notebooks.
- Find the right notebook with List notebooks before asking questions.
- Answer only from Ask notebook, and keep its citation numbers.
- When the user shares links, add them with Add sources and wait until they are ready.
- Before starting an Audio or Video Overview, confirm with the user: it uses their Google usage.
- If a generation is still running, never start it again: call Get job status with its jobid and wait=true until it finishes.
```

Then ask, for example: "Add https://en.wikipedia.org/wiki/Apollo_11 to my Apollo notebook and tell me why the landing nearly aborted."

## Waiting, limits and errors

- **Timing.** Chat answers in 15 to 30 seconds (up to about 80 seconds on busy accounts). Discover sources takes about 15 seconds, Deep Research 3 to 5 minutes, an Audio Overview 3 to 10 minutes, a Video Overview 10 minutes or more. The plugin polls every 15 seconds and waits 120 seconds per call by default, so an agent can check a long job over a few turns with **Get job status** instead of blocking. Workflows can raise the wait to 540 seconds, below Dify's default 600-second plugin limit (`PLUGIN_MAX_EXECUTION_TIMEOUT`). A job keeps running after the call returns, and jobs are kept for 30 days.
- **Usage.** Each Google account has Gemini Notebook's own usage budget, refilled every 5 hours plus a weekly budget. **Get account usage** shows what is left. Connect more Google accounts to generate more.
- **Errors** come back as one readable message, for example: an invalid token (401), an expired subscription (402), an id from another token (403), a missing notebook or an account that is not connected (404), sources still processing (409), the account busy or out of usage with its reset time (429), Google signing the account out (596, with the re-add link), and Google being temporarily unavailable (5xx).

## Privacy

The plugin sends requests only to `api.useapi.net` and stores nothing. See [PRIVACY.md](./PRIVACY.md) and the useapi.net [Terms and Privacy Policy](https://useapi.net/docs/legal?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin).

## Support

- API reference: https://useapi.net/docs/api-gemini-notebook-v1
- Examples (Node.js, Python, bash, n8n, Colab, an agent skill and this plugin's source): https://github.com/useapi/notebooklm-api
- Email support@useapi.net, or ask on [Discord](https://discord.gg/w28uK3cnmF) or [Telegram](https://t.me/use_api).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## Development

The tool YAML and Python stubs are generated from `dev/specs.py`, the single source of the parameters and their four UI languages (English, Simplified Chinese, Japanese, Brazilian Portuguese):

```bash
python dev/gen_tools.py                 # writes tools/*.yaml, tools/*.py and the provider YAML
python -m pytest                        # every tool against a mocked HTTP layer
python dev/routing_check.py             # live 401 check of every read-only endpoint with a fake token
dify plugin package . -o notebooklm_useapi-0.1.1.difypkg
```

`dev/` and `tests/` are left out of the package by `.difyignore`.
