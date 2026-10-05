# NotebookLM podcast: an agent skill

An [Agent Skill](https://agentskills.io) that lets Claude Code, Codex and other coding agents turn web pages, YouTube videos, pasted text and local files (PDF, Word, EPUB, audio...) into a NotebookLM **Audio Overview** podcast (`.m4a`) or a **Video Overview** (`.mp4`). Ask your agent "make a NotebookLM podcast from these three articles" and it runs the scripts in this folder.

It calls the [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill) by [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill), a third-party REST API that runs on your own Google NotebookLM account (NotebookLM is now called Gemini Notebook).

## Install

With the [skills CLI](https://github.com/vercel-labs/skills) (asks which agents to install for):

```bash
npx skills add useapi/notebooklm-api --skill notebooklm-podcast
# add -g to install for your user instead of the current project
```

Or copy the folder yourself:

```bash
git clone https://github.com/useapi/notebooklm-api.git
cp -r notebooklm-api/skills/notebooklm-podcast ~/.claude/skills/     # Claude Code, every project
cp -r notebooklm-api/skills/notebooklm-podcast .claude/skills/       # Claude Code, this project only
cp -r notebooklm-api/skills/notebooklm-podcast ~/.codex/skills/      # Codex
```

Then give the agent your token in the environment it runs in:

```bash
export USEAPI_TOKEN=user:12345-...      # your useapi.net API token
export USEAPI_EMAIL=you@gmail.com       # optional: which connected Google account to use
```

You need:

1. A useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill). One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill) covers every useapi.net API.
2. A Google account connected with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill). Generation runs on that account's own NotebookLM plan, the free one included.
3. `bash`, `curl` and [`jq`](https://jqlang.org/download/).

## Use it without an agent

The scripts work on their own too:

```bash
./scripts/podcast.sh "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=brief length=short
```

| Script | What it does |
|---|---|
| `scripts/podcast.sh` | Everything below in one command: links and files in, `.m4a` out |
| `scripts/create-notebook.sh` | Create a notebook, print its id |
| `scripts/add-sources.sh` | Add web pages, YouTube videos and pasted text |
| `scripts/upload-file.sh` | Upload a PDF, DOCX, PPTX, EPUB, Markdown, text, CSV, audio, video or image file |
| `scripts/wait-sources.sh` | Wait until Google has processed every source |
| `scripts/generate.sh` | Start an Audio Overview (`audio`) or a Video Overview (`video`), print the job id |
| `scripts/wait-job.sh` | Poll the job until it is done, print the final record |
| `scripts/download.sh` | Download the finished `.m4a` / `.mp4` |

[`SKILL.md`](./SKILL.md) is what the agent reads: the steps, every option and what to do on each error. The full API reference is at [useapi.net/docs/api-gemini-notebook-v1](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=skill&utm_campaign=notebooklm-skill).
