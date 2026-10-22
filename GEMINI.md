# Gemini Notebook (NotebookLM) via useapi.net

This extension connects the hosted useapi.net Gemini Notebook (NotebookLM) MCP server (`useapi-gemini-notebook`, 57 tools). The tools create notebooks, add sources (links, YouTube, files, Google Drive), chat with citations, run Deep Research and make every Studio output: Audio and Video Overviews, slides, infographics, reports, quizzes, flashcards and mind maps, on your Google AI subscription, the free plan included.

- Endpoint: https://api.useapi.net/v1/gemini-notebook/mcp (Streamable HTTP), authorized with the user's useapi.net API token in `USEAPI_TOKEN`.
- Before the tools work, the user needs a useapi.net API token (https://useapi.net/docs/start-here/setup-useapi) and a Google account connected at https://useapi.net/docs/start-here/setup-gemini-notebook.
- If a tool returns 401, ask the user to check `USEAPI_TOKEN` (`gemini extensions config useapi-notebooklm`). If it says no account is configured, point them to the setup page above.
- Generations use the Gemini Notebook usage of the user's Google AI subscription. Ask before starting many or long jobs, and report job status and links when they finish.
- Full tool list and limits: https://useapi.net/docs/api-gemini-notebook-v1/mcp

The extension also ships the `notebooklm-podcast` agent skill from `skills/`, which calls the same API with curl and reads `USEAPI_TOKEN` from the environment.

useapi.net is a paid third-party API service ($15/month covers every useapi.net API and 3 Google accounts), not affiliated with Google.
