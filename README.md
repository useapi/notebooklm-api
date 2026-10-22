# Gemini Notebook API (NotebookLM API) examples

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/useapi/notebooklm-api/blob/main/notebooks/notebooklm_podcast.ipynb)

Runnable Node.js, Python and bash examples, an agent skill, a Colab notebook and n8n workflows for the Gemini Notebook API (NotebookLM API): the [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) by [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), a third-party REST API that drives Google Gemini Notebook (formerly NotebookLM) on your [Google AI subscription](https://gemini.google/subscriptions/): Free, Plus $4.99, Pro $19.99, Ultra $99.99 or Ultra $199.99 a month (as of October 2026). Create notebooks, add web pages, YouTube videos, Drive files and uploads as sources, chat with citations, run Deep Research, and generate Audio Overviews (the Gemini Notebook podcast), Video Overviews, slide decks, infographics, reports, quizzes, flashcards and mind maps.

Google offers no Gemini Notebook API for regular Google accounts, and this one works on the free plan too. useapi.net is not affiliated with Google.

It runs unattended. Connect several Google accounts and each new job goes to one that is healthy and still has usage left, jobs are tracked server-side (poll or get a `replyUrl` webhook), and when every account is out of usage the `429` carries the reset time. Your code decides what to do with the load (wait, route to another account, slow down), so nobody has to watch Gemini Notebook's limits or start the next batch by hand.

| Example | What it does | Tutorial | Tutorial date |
|---|---|---|---|
| [`podcast/`](./podcast) | Turn web pages and YouTube videos into a Gemini Notebook Audio Overview and download the `.m4a` | [How to automate Gemini Notebook](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`deep-research/`](./deep-research) | Run Deep Research on a question and save the report as Markdown with its cited sources | [How to automate Gemini Notebook](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`tutorial-demo/`](./tutorial-demo) | The tutorial's two bash scripts: every step from creating a notebook to a Video Overview and a revised slide deck | [How to automate Gemini Notebook](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) | September 29, 2026 |
| [`skills/notebooklm-podcast/`](./skills/notebooklm-podcast) | An agent skill for Claude Code, Codex and other agents: links, text and files → Audio Overview `.m4a` or Video Overview `.mp4` (bash and curl) | [Skill README](./skills/notebooklm-podcast) | October 4, 2026 |
| [`notebooks/`](./notebooks) | A Google Colab notebook: paste your token, list your links, play the podcast inline and download it | [Open in Colab](https://colab.research.google.com/github/useapi/notebooklm-api/blob/main/notebooks/notebooklm_podcast.ipynb) | October 4, 2026 |
| [`n8n/`](./n8n) | n8n workflows: the Gemini Notebook (NotebookLM) Podcast App (a form and a weekly RSS feed, with an in-browser player), plus minimal links → podcast and RSS → podcast versions | [n8n README](./n8n) | October 5, 2026 |
| [`dify-plugin/`](./dify-plugin) | A Dify tool plugin: 56 Gemini Notebook tools for Dify [workflows, chatflows](https://docs.dify.ai/en/cloud/use-dify/build/workflow-chatflow) and [agents](https://docs.dify.ai/en/cloud/use-dify/build/new-agent/overview) (notebooks, sources, cited chat, Deep Research, Audio and Video Overviews, slides, reports, quizzes, mind maps), with files returned to Dify and a UI in English, Chinese, Japanese and Portuguese | [Plugin README](./dify-plugin) | October 18, 2026 |

## Quick start

You need [Node.js](https://nodejs.org) 21 or newer, or [Python](https://www.python.org) 3.8 or newer (no dependencies to install), a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), and a Google account connected with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) covers every useapi.net API. Connecting a Google account by hand? The [Google Account Setup](https://github.com/useapi/google-account-setup) scripts (Windows, macOS, Linux) open a clean, single-use Brave profile with device-bound sessions switched off, so the cookies you copy keep working.

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

useapi.net also runs a hosted [Model Context Protocol](https://modelcontextprotocol.io) server for Gemini Notebook (NotebookLM), so an AI assistant such as Claude Code, Cursor or VS Code Copilot can work with your notebooks on your Google account. It has 57 tools: notebooks, sources (links, YouTube, files, Google Drive, Google Play Books), chat with citations, notes, labels, sharing, collections, Deep Research and every Studio output (Audio and Video Overviews, slides, infographics, reports, tables, quizzes, flashcards, mind maps). Nothing to install or run locally, and no cookies to copy: you connect the account once and we keep it signed in.

- Endpoint: `https://api.useapi.net/v1/gemini-notebook/mcp`
- Transport: Streamable HTTP
- Authorization: your useapi.net API token in the `Authorization: Bearer …` header, and a Google account connected with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
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

VS Code, Windsurf and the full tool list: [Gemini Notebook MCP server (NotebookLM MCP server) docs](https://useapi.net/docs/api-gemini-notebook-v1/mcp?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). useapi.net is a third-party API, not affiliated with Google.

## Use with Claude Code

This repo is also a Claude Code plugin marketplace. The plugin adds the hosted Gemini Notebook MCP server (NotebookLM MCP server) and the `notebooklm-podcast` agent skill, and reads your token from the `USEAPI_TOKEN` environment variable, so set it before you start Claude Code:

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

## Use in Dify

The [`dify-plugin/`](./dify-plugin) folder is a [Dify](https://dify.ai) tool plugin, "Gemini Notebook (NotebookLM) by useapi.net", with 56 tools for [workflows, chatflows](https://docs.dify.ai/en/cloud/use-dify/build/workflow-chatflow) and [agents](https://docs.dify.ai/en/cloud/use-dify/build/new-agent/overview): notebooks, sources (links, YouTube, text, Google Drive, file uploads), chat with citations, Deep Research, and every Studio output. Generation tools wait for the job and return the Audio Overview `.m4a`, Video Overview `.mp4`, slides `.pdf`/`.pptx` or infographic `.png` as Dify files, plus variables (`notebook`, `jobid`, `answer`, `text`) for the next node.

1. Install it from the [Dify Marketplace](https://marketplace.dify.ai/plugins/useapi/notebooklm_useapi), or download the `.difypkg` from [Releases](https://github.com/useapi/notebooklm-api/releases) and upload it under Plugins > Install plugin > Local package file.
2. In Tools, authorize "Gemini Notebook (NotebookLM) by useapi.net" with your useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), and optionally a default Google account email.
3. Add a tool to a workflow. For links to a podcast in one node, use "Generate Audio Overview (podcast)" with `urls` set to your links: it creates the notebook, waits, and returns the `.m4a`.

The labels are in English, Simplified Chinese, Japanese and Brazilian Portuguese. Setup, every tool with its endpoint, and workflow and agent examples: [Dify plugin README](./dify-plugin).

## Articles and videos

- [Gemini Notebook (NotebookLM) API Options in 2026: Google Enterprise API, Free Libraries or a Hosted API](https://useapi.net/docs/articles/notebooklm-api-options?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [How to Automate Gemini Notebook (NotebookLM) with the API: Deep Research, Chat, Audio Overviews and a Lot More](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [Turn a Web Page or YouTube Video into a Podcast with Gemini Notebook (NotebookLM): A Real Example](https://useapi.net/docs/articles/notebooklm-podcast-example?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [How to Turn Web Pages, YouTube Videos and RSS Feeds into Gemini Notebook (NotebookLM) Podcasts with n8n](https://useapi.net/docs/articles/notebooklm-n8n-podcast?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [Chinese-language tutorial (中文教程): 用 Gemini Notebook API（NotebookLM API）生成中文播客](https://useapi.net/docs/articles/gemini-notebook-api-zh?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- YouTube: [NotebookLM has no API. Now it does: podcasts, video, slides from one REST call](https://www.youtube.com/shorts/ISOQAabo0b0)

## Common questions

<!-- Official API figures in these answers, re-read 2026-10-20 (useapi.net/docs/api-gemini-notebook-v1 sources): https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks (Preview, Enterprise licenses in a Google Cloud project: notebooks, sources, sharing and Audio Overviews only). Plans: https://gemini.google/subscriptions/ (Free, Plus $4.99, Pro $19.99, Ultra $99.99 or $199.99) read 2026-10-20. Google publishes no per-plan usage figures beyond notebook and source limits (overview Pricing). -->

- **Does Gemini Notebook (NotebookLM) have an API?** Yes, through useapi.net, for regular Google accounts: the useapi.net Gemini Notebook API runs on your Google AI subscription, the free plan included, with chat with citations, Deep Research and every Studio output. Google's own [Gemini Notebook Enterprise API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) needs Enterprise licenses in a Google Cloud project and covers only notebooks, sources, sharing and Audio Overviews, so regular Google accounts can't use it (as of October 2026).
- **Where do I get an API key / token?** Through useapi.net: you call Gemini Notebook with a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), since Google issues no Gemini Notebook API key for regular accounts. Connect your Google account once through the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api): sign in with Google, with no cookies to copy and no Google Cloud project. We keep the session signed in, and if Google ever signs it out, you get an email with a one-minute re-add link.
- **How much does it cost?** Through useapi.net, a podcast, video or answer has no price of its own: it uses the Gemini Notebook usage of your Google AI subscription, and the free plan works. A paid Google AI plan raises that usage, while Google's Enterprise API needs paid per-user licenses in a Google Cloud project (as of October 2026). See the [plan comparison](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api#pricing).
- **How many podcasts can I make?** Through useapi.net, as many as your connected Google accounts' usage allows: each account's Gemini Notebook usage refills every 5 hours up to a weekly limit. Connect more Google accounts with [POST /accounts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-accounts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), 3 per useapi.net subscription and up to 100 in total, and new jobs go automatically to an account that is healthy and still has usage left.
- **Can I generate Gemini Notebook (NotebookLM) podcasts with the API?** Through useapi.net, yes: podcasts (Audio Overviews) and Video Overviews too, which Google's Enterprise API doesn't offer (as of October 2026). Send links or text to [POST /artifacts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) and download the podcast as `.m4a`, a Video Overview as `.mp4`, slides as `.pdf` and `.pptx` or an infographic as `.png`. The [`podcast/`](./podcast) example does it in one run.
- More answers: [Gemini Notebook API questions](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api#questions).

## License

The example code in this repository is released under the [MIT License](./LICENSE). It covers the example scripts only, not the useapi.net service or API.

## About useapi.net

[useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) provides third-party REST APIs for AI services that run on your subscriptions to them: Google Flow, Google Vids, Muse, Gemini Notebook (NotebookLM), Dreamina, Kling, PixVerse, Mureka, Flow Music, MiniMax, Runway and more. See the [model matrix](https://useapi.net/model-matrix?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

Visit our [Discord Server](https://discord.gg/w28uK3cnmF) or [Telegram Channel](https://t.me/use_api) for any support questions and concerns.
