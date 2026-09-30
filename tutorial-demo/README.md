# The tutorial scripts

📖 Full walkthrough: [How to Automate NotebookLM with the Gemini Notebook API](https://useapi.net/docs/articles/gemini-notebook-bash)

The two bash scripts from the tutorial, unchanged. They need `curl` and `jq`, and save every response under a timestamped folder.

```bash
# steps 1–14: notebook, sources, upload, chat, note, discovery, Deep Research, quiz, Audio Overview, infographic, report, sharing
USEAPI_TOKEN=user:12345-... EMAIL=you@gmail.com ./gemini-notebook-demo.sh [path/to/file.pdf]

# steps 15–19: follow-up chat, note → source, flashcards, mind map, report, data table, Video Overview, slides + revise one slide
USEAPI_TOKEN=user:12345-... EMAIL=you@gmail.com NOTEBOOK=<id> CONVERSATION=<id> NOTE=<id> ./gemini-notebook-gallery.sh
```

The second script takes the notebook, conversation and note ids the first one prints.
