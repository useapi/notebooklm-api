# NotebookLM API (Gemini Notebook API) examples

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/useapi/notebooklm-api/blob/main/notebooks/notebooklm_podcast.ipynb)

Runnable Node.js, Python and bash examples, an agent skill, a Colab notebook and n8n workflows for the **NotebookLM API**: the [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) by [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), a REST API that drives Google **NotebookLM** (now called **Gemini Notebook**) on your own Google account. Create notebooks, add web pages, YouTube videos, Drive files and uploads as sources, chat with citations, run **Deep Research**, and generate **Audio Overviews** (the NotebookLM podcast), **Video Overviews**, slide decks, infographics, reports, quizzes, flashcards and mind maps.

Google offers no NotebookLM API for regular Google accounts. This API is third-party and uses the NotebookLM plan you already have.

It runs unattended. Connect several Google accounts and each new job goes to one that is healthy and still has usage left, jobs are tracked server-side (poll or get a `replyUrl` webhook), and when every account is out of usage the `429` carries the reset time. Your code decides what to do with the load (wait, route to another account, slow down), so nobody has to watch NotebookLM's limits or start the next batch by hand.

| Example | What it does | Tutorial | Tutorial date |
|---|---|---|---|
| [`podcast/`](./podcast) | Turn web pages and YouTube videos into a NotebookLM **Audio Overview** and download the `.m4a` | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`deep-research/`](./deep-research) | Run **Deep Research** on a question and save the report as Markdown with its cited sources | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`tutorial-demo/`](./tutorial-demo) | The tutorial's two bash scripts: every step from creating a notebook to a Video Overview and a revised slide deck | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`skills/notebooklm-podcast/`](./skills/notebooklm-podcast) | An **agent skill** for Claude Code, Codex and other agents: links, text and files → Audio Overview `.m4a` or Video Overview `.mp4` (bash + curl) | [Skill README](./skills/notebooklm-podcast) | October 4, 2026 |
| [`notebooks/`](./notebooks) | A **Google Colab** notebook: paste your token, list your links, play the podcast inline and download it | [Open in Colab](https://colab.research.google.com/github/useapi/notebooklm-api/blob/main/notebooks/notebooklm_podcast.ipynb) | October 4, 2026 |
| [`n8n/`](./n8n) | **n8n** workflows: the NotebookLM Podcast App (form + weekly RSS, in-browser player), plus minimal links → podcast and RSS → podcast versions | [n8n README](./n8n) | October 5, 2026 |

## Quick start

You need [Node.js](https://nodejs.org) 21+ **or** [Python](https://www.python.org) 3.8+ (no dependencies to install), a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), and a Google account connected with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) covers every useapi.net API.

```bash
git clone https://github.com/useapi/notebooklm-api.git
cd notebooklm-api/podcast
node ./podcast.mjs <API_TOKEN> <EMAIL>
# or, equivalently, with Python:
python3 ./podcast.py <API_TOKEN> <EMAIL>
```

Edit `prompts.json` in each folder to queue your own sources or questions. Every parameter is documented in the [API reference](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), and a [Postman collection](https://www.postman.com/useapinet/useapi-net/collection/29112081-40696e39-d128-417e-984b-fe1b97e7bb00) is available too.

No terminal? [Open the Colab notebook](https://colab.research.google.com/github/useapi/notebooklm-api/blob/main/notebooks/notebooklm_podcast.ipynb) and run it in your browser. Using Claude Code, Codex or another coding agent? Install the skill and ask for a podcast in plain words:

```bash
npx skills add useapi/notebooklm-api --skill notebooklm-podcast
```

## MCP server

useapi.net also runs a hosted [Model Context Protocol](https://modelcontextprotocol.io) server for NotebookLM (Gemini Notebook), so an AI assistant such as Claude Code, Cursor or VS Code Copilot can work with your notebooks on your own Google account. It has 57 tools: notebooks, sources (links, YouTube, files, Google Drive, Google Play Books), chat with citations, notes, labels, sharing, collections, Deep Research and every Studio output (Audio and Video Overviews, slides, infographics, reports, tables, quizzes, flashcards, mind maps). Nothing to install or run locally, and no cookies to copy: you connect the account once and we keep it signed in.

- Endpoint: `https://api.useapi.net/v1/gemini-notebook/mcp`
- Transport: Streamable HTTP
- Authorization: your useapi.net API token in the `Authorization: Bearer …` header, and a Google account connected with the [NotebookLM setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- Listed in the official MCP Registry as `net.useapi/gemini-notebook`

Claude Code:

```bash
claude mcp add --transport http useapi-gemini-notebook https://api.useapi.net/v1/gemini-notebook/mcp --header "Authorization: Bearer YOUR_API_TOKEN"
```

Cursor (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "useapi-gemini-notebook": {
      "url": "https://api.useapi.net/v1/gemini-notebook/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

VS Code, Windsurf and the full tool list: [NotebookLM MCP server docs](https://useapi.net/docs/api-gemini-notebook-v1/mcp?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). useapi.net is a third-party API, not affiliated with Google.

## Use with Claude Code

This repo is also a Claude Code plugin marketplace. The plugin adds the hosted NotebookLM (Gemini Notebook) MCP server and the `notebooklm-podcast` agent skill, and reads your token from the `USEAPI_TOKEN` environment variable, so set it before you start Claude Code:

```bash
export USEAPI_TOKEN=user:12345-...      # your useapi.net API token
```

Then, inside Claude Code:

```
/plugin marketplace add useapi/notebooklm-api
/plugin install notebooklm@useapi-notebooklm
```

On Claude Code 2.1.275 or later, `/plugin install notebooklm --marketplace useapi/notebooklm-api` does both in one step. Run `/mcp` to check that `useapi-gemini-notebook` is connected.

## Use with Gemini CLI

This repo is also a Gemini CLI extension with the same MCP server and the `notebooklm-podcast` agent skill:

```bash
gemini extensions install https://github.com/useapi/notebooklm-api
```

The install asks for your useapi.net API token and keeps it in the system keychain. Change it later with `gemini extensions config useapi-notebooklm`, and check the connection with `gemini mcp list`. The `notebooklm-podcast` skill's scripts read `USEAPI_TOKEN` from your shell, so export it as well if you use the skill.

## Common questions

<!-- Official API figures in these answers, verified 2026-10-18: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks (Enterprise licenses only). -->

- **Does NotebookLM have an API?** Yes, through the useapi.net NotebookLM API (Gemini Notebook API), a third-party REST API that drives your own Google account, so it works on free and paid consumer plans and covers everything in the web app: chat with citations, Deep Research and every Studio output. Google offers an API only for Gemini Notebook Enterprise (NotebookLM's new name since July 2026), which needs Enterprise licenses in a Google Cloud project and covers creating, listing, sharing and deleting notebooks, adding sources and generating Audio Overviews ([Google's docs](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks)), so regular Google accounts can't use it.
- **Where do I get an API key / token?** You call this API with a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) and connect your Google account once through the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api): sign in with Google, no cookies to copy and no Google Cloud project. Google doesn't issue a NotebookLM API key for regular accounts.
- **Connecting an account by hand instead?** The [Google Account Setup](https://github.com/useapi/google-account-setup) scripts (Windows, macOS, Linux) open a clean, single-use Brave profile with device-bound sessions switched off, so the cookies you copy keep working.
- **How much does it cost?** A flat [$15/month](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) to useapi.net, which covers every useapi.net API, not only this one. Generation runs on your own Google account's NotebookLM plan, the free one included, so there's no per-call or per-podcast charge from us. Google's own API needs Enterprise licenses in a Google Cloud project, so a regular account can't use it at any price.
- **How many podcasts can I make?** Each Google account has NotebookLM's own usage budget, which refills every 5 hours, plus a weekly one (see [how much one account can generate](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)). To make more, connect several Google accounts with [POST /accounts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-accounts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api): each subscription covers 3, up to 100 in total, and new jobs are load-balanced automatically to an account that is healthy and still has usage left.
- **What can I generate?** Audio Overviews (deep dive, brief, critique or debate; three lengths; output language of your choice), Video Overviews, slide decks (PDF + PPTX), infographics, reports, quizzes, flashcards, mind maps and data tables. See the [artifacts endpoint](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).
- More answers: [Gemini Notebook API questions](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api#questions).

## License

The example code in this repository is released under the [MIT License](./LICENSE). It covers the example scripts only, not the useapi.net service or API.

## About useapi.net

[useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) provides REST APIs for AI services on your own accounts: Google Flow, Flow Music, Gemini Notebook, Dreamina, Kling, PixVerse, MiniMax, Mureka, Runway and more. See the [model matrix](https://useapi.net/model-matrix?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

Visit our [Discord Server](https://discord.gg/w28uK3cnmF) or [Telegram Channel](https://t.me/use_api) for any support questions and concerns.
