# Gemini Notebook API (NotebookLM API) examples

English · [中文](#中文说明) · [日本語](#日本語の説明) · [Português](#sobre-este-repositório) · [Tiếng Việt](#về-repo-này) · [Bahasa Indonesia](#tentang-repo-ini) · [ไทย](#เกี่ยวกับ-repo-นี้)

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

- [Can You Use Your Google AI Subscription Through an API? What Plus, Pro and Ultra Get You](https://useapi.net/docs/articles/google-ai-subscription-api?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · Also in [中文](https://useapi.net/docs/articles/google-ai-subscription-api-zh?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · [日本語](https://useapi.net/docs/articles/google-ai-subscription-api-ja?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · [Português](https://useapi.net/docs/articles/google-ai-subscription-api-pt?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · [Tiếng Việt](https://useapi.net/docs/articles/google-ai-subscription-api-vi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · [Bahasa Indonesia](https://useapi.net/docs/articles/google-ai-subscription-api-id?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · [ไทย](https://useapi.net/docs/articles/google-ai-subscription-api-th?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [Gemini Notebook (NotebookLM) API Options in 2026: Google Enterprise API, Free Libraries or a Hosted API](https://useapi.net/docs/articles/notebooklm-api-options?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [How to Automate Gemini Notebook (NotebookLM) with the API: Deep Research, Chat, Audio Overviews and a Lot More](https://useapi.net/docs/articles/gemini-notebook-bash?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) · Also in [中文](https://useapi.net/docs/articles/gemini-notebook-api-zh?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [Turn a Web Page or YouTube Video into a Podcast with Gemini Notebook (NotebookLM): A Real Example](https://useapi.net/docs/articles/notebooklm-podcast-example?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- [How to Turn Web Pages, YouTube Videos and RSS Feeds into Gemini Notebook (NotebookLM) Podcasts with n8n](https://useapi.net/docs/articles/notebooklm-n8n-podcast?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)
- YouTube: [NotebookLM has no API. Now it does: podcasts, video, slides from one REST call](https://www.youtube.com/shorts/ISOQAabo0b0)

## Common questions

<!-- Official API figures in these answers, re-read 2026-10-20 (useapi.net/docs/api-gemini-notebook-v1 sources): https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks (Preview, Enterprise licenses in a Google Cloud project: notebooks, sources, sharing and Audio Overviews only). Plans: https://gemini.google/subscriptions/ (Free, Plus $4.99, Pro $19.99, Ultra $99.99 or $199.99) read 2026-10-20. Google publishes no per-plan usage figures beyond notebook and source limits (overview Pricing). -->

- **Does Gemini Notebook (NotebookLM) have an API?** Yes, through useapi.net, for regular Google accounts: the useapi.net Gemini Notebook API runs on your Google AI subscription, the free plan included, with chat with citations, Deep Research and every Studio output. Google's own [Gemini Notebook Enterprise API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) needs Enterprise licenses in a Google Cloud project and covers only notebooks, sources, sharing and Audio Overviews, so regular Google accounts can't use it (as of October 2026).
- **Where do I get an API key / token?** Through useapi.net: you call Gemini Notebook with a useapi.net [API token](https://useapi.net/docs/start-here/setup-useapi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), since Google issues no Gemini Notebook API key for regular accounts. Connect your Google account once through the [Gemini Notebook setup](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api): sign in with Google, with no cookies to copy and no Google Cloud project. We keep the session signed in, and if Google ever signs it out, you get an email with a one-minute re-add link.
- **How much does it cost?** Through useapi.net, a podcast, video or answer has no price of its own: it uses the Gemini Notebook usage of your Google AI subscription, and the free plan works. A paid Google AI plan raises that usage, while Google's Enterprise API needs paid per-user licenses in a Google Cloud project (as of October 2026). See the [plan comparison](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api#pricing).
- **How many podcasts can I make?** Through useapi.net, as many as your connected Google accounts' usage allows: each account's Gemini Notebook usage refills every 5 hours up to a weekly limit. Connect more Google accounts with [POST /accounts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-accounts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), 3 per useapi.net subscription and up to 100 in total, and new jobs go automatically to an account that is healthy and still has usage left.
- **Can I generate Gemini Notebook (NotebookLM) podcasts with the API?** Through useapi.net, yes: podcasts (Audio Overviews) and Video Overviews too, which Google's Enterprise API doesn't offer (as of October 2026). Send links or text to [POST /artifacts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) and download the podcast as `.m4a`, a Video Overview as `.mp4`, slides as `.pdf` and `.pptx` or an infographic as `.png`. The [`podcast/`](./podcast) example does it in one run.
- More answers: [Gemini Notebook API questions](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api#questions).

## 中文说明

这是 [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) 的 Gemini Notebook API（NotebookLM API）示例代码（Node.js、Python 和 bash），通过第三方 REST API 在你自己的 Google 账号上创建笔记本、添加网页和 YouTube 来源、带引用对话、运行 Deep Research，并生成 Audio Overview 播客、Video Overview、幻灯片和信息图。

- 使用你的 Google AI 订阅（免费版、Plus $4.99、Pro $19.99、Ultra $99.99 或 Ultra $199.99 每月），免费 Google 账号也能用。
- 无需 Google Cloud 项目或 API Key。Google 只为 Enterprise 许可证提供 Gemini Notebook API，普通 Google 账号用不了。
- 账号只需绑定一次：用 Google 登录即可，无需复制 Cookie，会话由我们保持登录。
- 不按次收费：播客和回答用的是你 Google 套餐自带的用量，每 5 小时刷新一次。按 Google 的估算，一个满额 5 小时窗口可启动 2 个（免费版）、9 个（Pro）或 181 个（Ultra $199.99）Audio Overview（2026 年 10 月）。useapi.net 每月 15 美元，含所有 API，每个订阅可绑定 3 个 Google 账号，总数最多 100 个。
- `podcast/` 把网页和 YouTube 视频生成播客并下载 `.m4a`，`deep-research/` 把 Deep Research 报告连同引用来源保存为 Markdown，另有 agent skill、Colab 笔记本、n8n 工作流和 Dify 插件。

中文教程（中文播客、PDF、信息图，含 curl 示例）：[如何用 Gemini Notebook API（NotebookLM API）把网页、PDF 和 YouTube 视频变成中文播客](https://useapi.net/docs/articles/gemini-notebook-api-zh?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)。完整文档：[Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)。

## 日本語の説明

[useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) の Gemini Notebook API（NotebookLM API）のサンプルです。Google Gemini Notebook（旧 NotebookLM）を動かすサードパーティの REST API で、ノートブック、ソース、引用付きのチャット、Deep Research、音声解説（ポッドキャスト）、動画解説、スライド、インフォグラフィック、レポートを扱えます。

- お使いの Google AI のプランで動きます：無料、Plus $4.99、Pro $19.99、Ultra $99.99、Ultra $199.99（月額、2026年10月時点）。無料プランでも使えます。
- Google Cloud プロジェクトも Gemini API キーも不要です。Google は通常のアカウントに Gemini Notebook の API キーを発行していないので、useapi.net のトークンで API を呼び出します。
- Google アカウントは、自動化されたブラウザーの手順で接続します。Google に一度ログインするだけで、Cookie をコピーする必要はありません。
- コスト：useapi.net は月 $15 で、すべての API と、サブスクリプションごとに3つの Google アカウントが含まれ、ポッドキャストごとの料金はかかりません。Google 側の利用分はお使いのプランから使われます。Google の見積もりでは、5時間の枠1つで開始できる音声解説は、無料プランで約2本、Google AI Pro で9本です（2026年10月時点）。
- サンプルでは、Web ページや YouTube 動画を `.m4a` のポッドキャストにし（`language: "ja"` で日本語にも）、Deep Research を実行してレポートを Markdown で保存します。エージェントスキル、Colab ノートブック、n8n のワークフロー、Dify のプラグインも入っています。

日本語の記事：[Gemini Notebook API（NotebookLM API）で Web ページ、PDF、YouTube 動画を日本語のポッドキャストにする方法](https://useapi.net/docs/articles/gemini-notebook-bash-ja?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)。ドキュメント全体：[Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)。

## Sobre este repositório

Exemplos da Gemini Notebook API (NotebookLM API) da [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), uma API REST de terceiros que controla o Google Gemini Notebook (antigo NotebookLM): notebooks, fontes, chat com citações, Deep Research, e Audio Overviews (podcasts), Video Overviews, slides, infográficos e relatórios.

- Roda na sua assinatura do Google AI: gratuita, Plus $4,99, Pro $19,99, Ultra $99,99 ou Ultra $199,99 por mês (outubro de 2026), e o plano gratuito funciona.
- Sem projeto no Google Cloud e sem chave da Gemini API: o Google não emite chave da Gemini Notebook API para contas comuns, e você chama a API com o token da useapi.net.
- A conta Google é conectada por um fluxo automatizado no navegador: você entra no Google uma vez, sem copiar cookies.
- Custo: a useapi.net custa $15 por mês, com todas as APIs e 3 contas Google por assinatura, sem cobrança por podcast. O uso do lado do Google vem do seu plano: pelas estimativas do Google, uma janela de 5 horas inicia cerca de 2 Audio Overviews no plano gratuito e 9 no Google AI Pro (outubro de 2026).
- Os exemplos transformam páginas web e vídeos do YouTube em um podcast `.m4a` (também em português, com `language: "pt_BR"`), rodam Deep Research e salvam o relatório em Markdown, e incluem uma skill para agentes, um notebook do Colab, workflows n8n e um plugin para o Dify.

Artigo em português: [Como usar a Gemini Notebook API (NotebookLM API) para transformar páginas web, PDFs e vídeos do YouTube em podcasts em português](https://useapi.net/docs/articles/gemini-notebook-bash-pt?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). Documentação completa: [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

## Về repo này

Ví dụ cho Gemini Notebook API (NotebookLM API) của [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), một REST API của bên thứ ba điều khiển Google Gemini Notebook (trước đây là NotebookLM): notebook, nguồn, chat có trích dẫn nguồn, Deep Research, cùng Audio Overview (podcast), Video Overview, slide, infographic và báo cáo.

- Chạy trên gói Google AI của bạn: Ultra $199,99, Ultra $99,99, Pro $19,99, Plus $4,99 mỗi tháng hoặc gói miễn phí (tháng 10/2026), và gói miễn phí cũng dùng được.
- Không cần dự án Google Cloud hay Gemini API key: Google không cấp Gemini Notebook API key cho tài khoản thông thường, và bạn gọi API bằng token của useapi.net.
- Tài khoản Google được kết nối bằng quy trình trình duyệt tự động: đăng nhập Google một lần, không cần chép cookie.
- Chi phí: useapi.net giá $15 mỗi tháng, gồm mọi API và 3 tài khoản Google mỗi gói đăng ký, không tính phí theo podcast. Mức dùng phía Google lấy từ gói của bạn: theo ước tính của Google, một khung 5 giờ bắt đầu được khoảng 2 Audio Overview trên gói miễn phí, 9 trên Google AI Pro và 181 trên Ultra $199,99 (tháng 11/2026).
- Các ví dụ biến trang web và video YouTube thành podcast `.m4a` (chọn ngôn ngữ bằng `language`), chạy Deep Research và lưu báo cáo dạng Markdown, kèm một agent skill, một notebook Colab, workflow n8n và plugin Dify.

Bài viết tiếng Việt: [Cách dùng Gemini Notebook API (NotebookLM API) biến trang web, PDF và video YouTube thành podcast](https://useapi.net/docs/articles/gemini-notebook-bash-vi?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). Tài liệu đầy đủ: [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

## Tentang repo ini

Ini adalah contoh kode Node.js, Python dan bash untuk Gemini Notebook API (NotebookLM API) dari [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api), API pihak ketiga yang menjalankan Google Gemini Notebook (dulu NotebookLM) lewat REST API: notebook, sumber dari web, YouTube, Drive dan file upload, tanya jawab dengan sitasi, Deep Research, Audio Overview (podcast), Video Overview, slide, infografis, laporan, kuis, flashcard dan mind map.

- Berjalan di paket Google AI Anda: Gratis, Plus $4,99, Pro $19,99, Ultra $99,99 atau Ultra $199,99 per bulan (per Oktober 2026), termasuk paket gratis. Podcast bisa dibuat dalam bahasa Indonesia dengan `language: "id"`.
- Tanpa project Google Cloud dan tanpa Gemini API key. Google hanya menyediakan Enterprise API yang butuh lisensi Enterprise di project Google Cloud dan tidak bisa dipakai akun Google biasa.
- Akun dihubungkan lewat [setup Gemini Notebook](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api): login ke Google, tanpa menyalin cookie. Hubungkan beberapa akun, dan setiap job baru otomatis diarahkan ke akun yang sehat dan masih punya kuota.
- Harga: langganan useapi.net $15 per bulan untuk semua API, dengan 3 akun Google per langganan (maksimal 100). Podcast tidak punya harga sendiri: kuota Notebook terisi ulang setiap 5 jam, dan satu jendela 5 jam bisa memulai sekitar 2 Audio Overview di akun gratis, 9 di Google AI Pro dan 181 di Google AI Ultra, menurut perkiraan Google.
- Contoh di repo: `podcast/` mengubah halaman web dan video YouTube menjadi Audio Overview `.m4a`, `deep-research/` menyimpan laporan Deep Research sebagai Markdown, ditambah notebook Google Colab, workflow n8n, plugin Dify dan agent skill untuk Claude Code dan Codex.

Artikel bahasa Indonesia: [Cara Memakai Gemini Notebook API (NotebookLM API): Ubah Web, PDF dan Video YouTube Menjadi Podcast Berbahasa Indonesia](https://useapi.net/docs/articles/gemini-notebook-bash-id?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api). Dokumentasi lengkap: [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

## เกี่ยวกับ repo นี้

นี่คือตัวอย่างโค้ด Node.js, Python และ bash สำหรับ Gemini Notebook API (NotebookLM API) ของ [useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) ซึ่งเป็น API ของบุคคลที่สาม ใช้สร้างโน้ตบุ๊ก เพิ่มแหล่งข้อมูลจากเว็บและ YouTube แชตพร้อมแหล่งอ้างอิง รัน Deep Research และสร้างพอดแคสต์ Audio Overview, Video Overview, สไลด์ และอินโฟกราฟิก บนบัญชี Google ของคุณเอง

- ใช้แพ็กเกจ Google AI ของคุณ (ฟรี, Plus $4.99, Pro $19.99, Ultra $99.99 หรือ Ultra $199.99 ต่อเดือน) บัญชี Google ฟรีก็ใช้ได้
- ไม่ต้องมีโปรเจกต์ Google Cloud หรือ API key ส่วน Gemini Notebook API ของ Google เองมีให้เฉพาะไลเซนส์ Enterprise บัญชี Google ทั่วไปใช้ไม่ได้
- เชื่อมบัญชีครั้งเดียวผ่าน[หน้าตั้งค่า](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) แค่ล็อกอิน Google ไม่ต้องคัดลอก cookie และเราดูแลให้เซสชันล็อกอินอยู่เสมอ
- ไม่คิดเงินต่อชิ้น: พอดแคสต์และคำตอบใช้โควตาที่มากับแพ็กเกจ Google ของคุณ ซึ่งรีเฟรชทุก 5 ชั่วโมง ตามตัวเลขประมาณของ Google รอบ 5 ชั่วโมงเต็มหนึ่งรอบเริ่ม Audio Overview ได้ 2 รายการ (ฟรี) 9 รายการ (Pro) หรือ 181 รายการ (Ultra $199.99) (ข้อมูล ณ ตุลาคม 2026) ค่าบริการ useapi.net คือ $15 ต่อเดือน รวมทุก API
- ตัวอย่างใน repo: `podcast/` เปลี่ยนหน้าเว็บและวิดีโอ YouTube เป็นพอดแคสต์แล้วดาวน์โหลดไฟล์ `.m4a` `deep-research/` บันทึกรายงาน Deep Research พร้อมแหล่งอ้างอิงเป็น Markdown และยังมี agent skill, โน้ตบุ๊ก Colab, workflow ของ n8n และปลั๊กอิน Dify

บทความภาษาไทย: [วิธีใช้ Gemini Notebook API (NotebookLM API) เปลี่ยนเว็บ PDF และวิดีโอ YouTube เป็นพอดแคสต์ภาษาไทย](https://useapi.net/docs/articles/gemini-notebook-bash-th?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) เอกสารฉบับเต็ม: [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api)

## License

The example code in this repository is released under the [MIT License](./LICENSE). It covers the example scripts only, not the useapi.net service or API.

## About useapi.net

[useapi.net](https://useapi.net/?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api) provides third-party REST APIs for AI services that run on your subscriptions to them: Google Flow, Google Vids, Muse, Gemini Notebook (NotebookLM), Dreamina, Kling, PixVerse, Mureka, Flow Music, MiniMax, Runway and more. See the [model matrix](https://useapi.net/model-matrix?utm_source=github.com&utm_medium=referral&utm_campaign=notebooklm-api).

Visit our [Discord Server](https://discord.gg/w28uK3cnmF) or [Telegram Channel](https://t.me/use_api) for any support questions and concerns.
