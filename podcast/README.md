# Audio Overview podcast from URLs

📖 Full walkthrough: [How to Automate NotebookLM with the Gemini Notebook API](https://useapi.net/docs/articles/gemini-notebook-bash)

For every entry in `prompts.json`, the script creates a notebook, adds the URLs as sources (web pages and YouTube videos), waits until Google has processed them, generates an **Audio Overview** with [POST /artifacts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts) (`type: "audio"`, async), polls [GET /jobs](https://useapi.net/docs/api-gemini-notebook-v1/get-gemini-notebook-jobs-jobid), and downloads the `.m4a`.

```bash
node podcast.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]
python3 podcast.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]
```

`prompts.json` entries: `title`, `urls` (1–50), and optional `format` (`deep_dive` default, `brief`, `critique`, `debate`), `length` (`short`, `default`, `long`) and `language` (`en`, `es`, `pt_BR`, `zh_Hans`, …). A short brief takes about 5 minutes.
