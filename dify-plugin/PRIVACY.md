# Privacy Policy

This privacy policy covers the "Gemini Notebook (NotebookLM) by useapi.net" Dify plugin (`useapi/notebooklm_useapi`).

## What the plugin sends, and where

The plugin sends requests to one place only: `https://api.useapi.net`, the useapi.net Gemini Notebook API. It contacts no other server. It does not send data to analytics services or to any other third party.

Each request carries:

- your useapi.net API token, in the `Authorization` header, so useapi.net can identify your subscription;
- the optional Google account email you set in the credentials or in a tool;
- the content of the tool call: notebook, source, artifact and job ids, questions, instructions, URLs, pasted text, and any file you upload as a source.

useapi.net runs the request on the Google account you connected to it. Your sources, questions and generated content are therefore processed by Google Gemini Notebook (NotebookLM) in that Google account.

## What the plugin stores

The plugin stores nothing. It keeps no logs, no cache and no copy of your data, and holds a request only while the tool runs. Dify stores your API token as an encrypted credential; the plugin does not.

Files the plugin returns to Dify (for example an Audio Overview `.m4a`) are stored by your Dify instance like any other tool output file.

## Data handled by the services the plugin calls

- **useapi.net** receives the requests above and keeps job records for 30 days. How useapi.net collects, uses and shares data is described in its Terms of Service and Privacy Policy: https://useapi.net/docs/legal
- **Google** processes your notebooks, sources and generated content in your Google account, under Google's Privacy Policy: https://policies.google.com/privacy

useapi.net is a third-party service. It is not affiliated with, endorsed by or sponsored by Google.

## Personal data

The plugin does not collect personal data for its own use. Personal data inside the content you send (for example, in a document you upload or text you paste) is sent to useapi.net and Google as described above, only because you asked a tool to process it. Do not send content you are not allowed to share with these services.

## Contact

Questions about this policy: support@useapi.net
