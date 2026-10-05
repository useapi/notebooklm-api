# n8n workflows for the NotebookLM (Gemini Notebook) API

Ready-to-import [n8n](https://n8n.io) workflows that turn links or an RSS feed into a NotebookLM **Audio Overview** (the two-host podcast). All of them use only core n8n nodes, with no community nodes. Tested on self-hosted n8n 2.41.

| Workflow | What it does |
|---|---|
| [`notebooklm-podcast-app.json`](./notebooklm-podcast-app.json) | **The full app.** A form and a weekly RSS schedule share one pipeline: pick format, length, language and a focus prompt, watch a progress panel, then play the podcast in the browser and download it. Unreachable links are skipped with a reason, and quota or account problems show a page that says what to do |
| [`notebooklm-podcast.json`](./notebooklm-podcast.json) | A form: paste web pages and YouTube links, pick a format and a length; the `.m4a` ends up as binary data in n8n for the next node (the browser gets a confirmation page, not the file) |
| [`notebooklm-rss-podcast.json`](./notebooklm-rss-podcast.json) | Every Monday, the newest posts of an RSS feed become one podcast episode |

📖 Full walkthrough: [How to Turn Web Pages, YouTube Videos and RSS Feeds into NotebookLM Podcasts with n8n](https://useapi.net/docs/articles/notebooklm-n8n-podcast?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)

The two smaller files are the minimal versions of the same pipeline, for building your own flow. The n8n.io listing for the app is pending review; until it is live, import the files from this folder.

## Podcast App (form + weekly RSS)

[`notebooklm-podcast-app.json`](./notebooklm-podcast-app.json) is the complete version: one workflow, two ways in.

- **The form "Make a podcast"** takes a title, up to 50 links (web pages and YouTube videos), a format (deep dive, brief, critique, debate), a length, one of 20 languages, an optional focus prompt and an optional Google account email. While Google reads the links and makes the episode, the page shows what is happening and a running clock. A sources page lists what Google read and what it skipped and why, and the result page plays the podcast in the browser, with a download link.
- **The weekly schedule** (Monday 7:00, off until you switch it on) reads the RSS feed in **Feed settings**, keeps the posts from the last `lookbackDays` days, and makes one episode. It ends at **Episode** with the `.m4a` as binary data, ready for a Google Drive, S3, Telegram or podcast-host node.
- **When something goes wrong**, the form shows a page that says what to do: a link Google could not reach is skipped (the others still go in), an account that is out of NotebookLM usage shows when it resets, and an account that needs reconnecting links to the setup page. Temporary errors are retried.

Setup: import the file, create one **Header Auth** credential (Name `Authorization`, Value `Bearer <your API token>`), select it on the eight HTTP Request nodes (Create notebook, Add sources, Add each link, Read notebook, Generate Audio Overview, Check job, Download podcast, Fetch audio), then publish (activate) the workflow and open the form URL. The **Podcast audio** webhook streams the finished episode to the result page using that credential, so your token never reaches the browser.

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

1. Get a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) and connect your Google account with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook).
2. In n8n, import the file (**Workflows → Import from File**).
3. Create a **Header Auth** credential. Name: `Authorization`. Value: `Bearer <your API token>`.
4. Select that credential on the six HTTP Request nodes: Create notebook, Add sources, Check sources, Generate Audio Overview, Check job and Download audio (the download link needs your token too).
5. Form workflow: activate it and open the form URL, or click **Execute workflow** to test it. RSS workflow: put your feed in **Feed settings**, click **Execute workflow** to try it, then publish (activate) it.

A short brief takes about 3 to 10 minutes. Add a Google Drive, S3, Telegram or podcast-host node after **Download audio** to send the episode where you need it.

## Errors

- **HTTP 429** on Generate Audio Overview: the Google account is out of NotebookLM usage for now. The response carries `retryAt` when Google names the reset time. Connect more Google accounts with [POST /accounts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-accounts) and leave `email` empty: new notebooks then go to the least busy account, so the next run can land on one that still has usage.
- **Job failed**: the workflow stops with the error Google returned.
- A source that ends as `error` (for example a YouTube video without captions) is skipped; the episode uses the rest.

One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) covers every useapi.net API. Generation runs on your own Google account's NotebookLM plan.
