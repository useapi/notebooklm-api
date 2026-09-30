# Deep Research report as Markdown

📖 Full walkthrough: [How to Automate NotebookLM with the Gemini Notebook API](https://useapi.net/docs/articles/gemini-notebook-bash)

For every question in `prompts.json`, the script creates a notebook, starts **Deep Research** with [POST /research](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-research) (`type: "deep"`, async), polls [GET /jobs](https://useapi.net/docs/api-gemini-notebook-v1/get-gemini-notebook-jobs-jobid), and saves the report (`.md`) plus the sources Google read (`.sources.json`, each marked `cited` or not). A run takes about 3–5 minutes.

```bash
node research.mjs <API_TOKEN> [EMAIL] [PROMPTS_FILE]
python3 research.py <API_TOKEN> [EMAIL] [PROMPTS_FILE]
```

A research run doesn't change the notebook. To keep the report or sources, import them with [POST /research/import](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-research-import).
