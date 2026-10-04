# n8n workflows for the NotebookLM (Gemini Notebook) API

Two ready-to-import [n8n](https://n8n.io) workflows that turn links into a NotebookLM **Audio Overview** (the two-host podcast). Both use only core n8n nodes, with no community nodes. Tested on self-hosted n8n 2.41.

| Workflow | What it does |
|---|---|
| [`notebooklm-podcast.json`](./notebooklm-podcast.json) | A form: paste web pages and YouTube links, pick a format and a length, get the `.m4a` back |
| [`notebooklm-rss-podcast.json`](./notebooklm-rss-podcast.json) | Every Monday, the newest posts of an RSS feed become one podcast episode |

The n8n.io listing for these templates is pending review. Until it is live, import the files from this folder.

## Links to podcast (form)

1. A form collects a title, the links (web pages and YouTube videos, one per line, up to 50), the podcast format (`deep_dive`, `brief`, `critique`, `debate`) and the length (`short`, `default`, `long`).
2. The workflow creates a notebook with [POST /notebooks](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-notebooks) and adds the links with [POST /sources](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-sources).
3. It checks the notebook every 10 seconds until Google has processed every source.
4. It starts the Audio Overview with [POST /artifacts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts) (`type: "audio"`, async), polls [GET /jobs](https://useapi.net/docs/api-gemini-notebook-v1/get-gemini-notebook-jobs-jobid) every 20 seconds, and downloads the `.m4a` as binary data for the next node.

Set `language` (for example `es`, `pt_BR`, `zh_Hans`) and, optionally, `email` in the **Settings** node.

## RSS feed to weekly podcast

1. A Schedule Trigger starts the run every Monday at 7:00.
2. **Read feed** fetches the feed in **Feed settings**. **Newest posts** keeps the posts published within `lookbackDays` (default 7), newest first, at most `maxPosts` (default 5). When there are no new posts, the run stops and no episode is made.
3. From there it is the same flow as above: one notebook titled `<showName>, <date>`, the post links as sources, one Audio Overview, the `.m4a` downloaded.

**Feed settings** holds `feedUrl`, `showName`, `maxPosts`, `lookbackDays`, `format`, `length`, `language` and `email`. If you change the schedule, change `lookbackDays` to match (for example a daily run with `lookbackDays: 1`).

## Setup

1. Get a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api) and connect your Google account with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook).
2. In n8n, import the file (**Workflows → Import from File**).
3. Create a **Header Auth** credential. Name: `Authorization`. Value: `Bearer <your API token>`.
4. Select that credential on the six HTTP Request nodes: Create notebook, Add sources, Check sources, Generate Audio Overview, Check job and Download audio (the download link needs your token too).
5. Form workflow: activate it and open the form URL, or click **Execute workflow** to test it. RSS workflow: put your feed in **Feed settings**, click **Execute workflow** to try it, then publish (activate) it.

A short brief takes about 3 to 10 minutes. Add a Google Drive, S3, Telegram or podcast-host node after **Download audio** to send the episode where you need it.

## Errors

- **HTTP 429** on Generate Audio Overview: the Google account is out of NotebookLM usage for now. The response carries `retryAt` when Google names the reset time. Connect more Google accounts with [POST /accounts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-accounts) and leave `email` empty: new notebooks are spread across them.
- **Job failed**: the workflow stops with the error Google returned.
- A source that ends as `error` (for example a YouTube video without captions) is skipped; the episode uses the rest.

One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api) covers every useapi.net API. Generation runs on your own Google account's NotebookLM plan.
