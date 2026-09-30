# Gemini Notebook (NotebookLM) API examples (useapi.net)

Runnable Node.js, Python and bash examples for the [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1) by [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api), a REST API for Google's **Gemini Notebook** (formerly **NotebookLM**) that drives your own Google account. Create notebooks, add web pages, YouTube videos, Drive files and uploads as sources, chat with citations, run **Deep Research**, and generate **Audio Overviews** (the NotebookLM podcast), **Video Overviews**, slide decks, infographics, reports, quizzes, flashcards and mind maps.

Google offers no public API for NotebookLM. This API is third-party and uses the NotebookLM plan you already have.

| Example | What it does | Tutorial | Tutorial date |
|---|---|---|---|
| [`podcast/`](./podcast) | Turn web pages and YouTube videos into a NotebookLM **Audio Overview** and download the `.m4a` | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash) | September 29, 2026 |
| [`deep-research/`](./deep-research) | Run **Deep Research** on a question and save the report as Markdown with its cited sources | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash) | September 29, 2026 |
| [`tutorial-demo/`](./tutorial-demo) | The tutorial's two bash scripts: every step from creating a notebook to a Video Overview and a revised slide deck | [How to automate NotebookLM](https://useapi.net/docs/articles/gemini-notebook-bash) | September 29, 2026 |

## Quick start

You need [Node.js](https://nodejs.org) 21+ **or** [Python](https://www.python.org) 3.8+ (no dependencies to install), a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api), and a Google account connected with the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook). One [$15/month subscription](https://useapi.net/docs/subscription?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api) covers every useapi.net API.

```bash
git clone https://github.com/useapi/gemini-notebook-api.git
cd gemini-notebook-api/podcast
node ./podcast.mjs <API_TOKEN> <EMAIL>
# or, equivalently, with Python:
python3 ./podcast.py <API_TOKEN> <EMAIL>
```

Edit `prompts.json` in each folder to queue your own sources or questions. Every parameter is documented in the [API reference](https://useapi.net/docs/api-gemini-notebook-v1), and a [Postman collection](https://www.postman.com/useapinet/useapi-net/collection/29112081-40696e39-d128-417e-984b-fe1b97e7bb00) is available too.

## Common questions

- **Does NotebookLM have an API?** Not a public one for the consumer product. This third-party REST API drives your own Gemini Notebook account instead.
- **What can I generate?** Audio Overviews (deep dive, brief, critique or debate; three lengths; output language of your choice), Video Overviews, slide decks (PDF + PPTX), infographics, reports, quizzes, flashcards, mind maps and data tables. See the [artifacts endpoint](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts).
- **What does it cost?** A flat $15/month to useapi.net plus the Google plan you already have. There's no per-call metering.

## License

The example code in this repository is released under the [MIT License](./LICENSE). It covers the example scripts only, not the useapi.net service or API.

## About useapi.net

[useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api) provides REST APIs for AI services on your own accounts: Google Flow, Flow Music, Gemini Notebook, Dreamina, Kling, PixVerse, MiniMax, Mureka, Runway and more. See the [model matrix](https://useapi.net/model-matrix?utm_source=github.com&utm_medium=referral&utm_campaign=gemini-notebook-api).

Visit our [Discord Server](https://discord.gg/w28uK3cnmF) or [Telegram Channel](https://t.me/use_api) for any support questions and concerns.
