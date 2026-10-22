# Changelog

## 0.1.2 (2026-10-22)

Name and wording only. No functional changes.

- Changed: the plugin is now called "Gemini Notebook (NotebookLM) by useapi.net", leading with Gemini Notebook after Google renamed NotebookLM. NotebookLM stays in the name, in all four languages.
- Changed: the plugin descriptions say the plugin runs on your Google AI subscription (free plan included), the Audio Overview tool description and a few error messages use the new name order, and the README, PRIVACY.md and localized READMEs show the new label.
- No breaking changes: the plugin id (`useapi/notebooklm_useapi`), tool names, parameters and output variables are unchanged.

## 0.1.1 (2026-10-19)

Fixes for Dify agents, found in a Dify Cloud agent test.

- Fixed: a tool could send a workflow variable with an empty value (for example `text` = "" after an Audio Overview, which has no text). Dify's agent runtime reports that as a tool invoke error, so the agent retried and started the generation again. Empty variables, texts and links are no longer sent by any tool, an empty JSON result is wrapped, and every tool now sends its readable text first.
- Changed: generation tools (Audio and Video Overview, slides, infographic, report, interactive report, data table, quiz, flashcards, mind map, suggested item, retry, revise slide), Research, Get job status and the source tools now wait up to 120 seconds by default instead of 180 to 540, so an agent turn stays short. Workflows can still raise "Maximum wait" to 540 seconds.
- Changed: a job that is still running returns a clear message with its `jobid`, telling the agent to call Get job status (`get_job`) with `wait=true` and not to start the generation again. The `jobid`, `status`, `notebook` and `artifact` variables are set as before.
- Changed: an empty chat answer from Google is reported as an error instead of an empty result.
- No breaking changes: tool names, parameters and output variables are unchanged.

## 0.1.0 (2026-10-18)

First release.

- 56 tools covering the useapi.net Gemini Notebook API (NotebookLM): accounts and jobs, notebooks, sharing, sources (URLs, YouTube, text, Google Drive, Google Play Books, file upload), source search, cited chat, chat settings, Discover sources and Deep Research, notes, labels and collections.
- Every Studio output: Audio Overview (podcast), Video Overview, slide deck, infographic, report, interactive report, data table, quiz, flashcards and mind map, from a notebook or one-shot from URLs and text.
- Generation tools wait for the job (up to 540 seconds) and return the audio, video, PDF, PPTX or PNG as Dify files, plus readable text and workflow variables (`jobid`, `status`, `notebook`, `artifact`, `text`, `file_urls`).
- Interface in English, Simplified Chinese, Japanese and Brazilian Portuguese.
