# NotebookLM（Gemini Notebook），由 useapi.net 提供

**作者：** useapi · **版本：** 0.1.1 · **类型：** 工具 · **源代码：** https://github.com/useapi/notebooklm-api/tree/main/dify-plugin · **联系方式：** support@useapi.net

在 Dify 的工作流、Chatflow 和 Agent 中使用 Google **NotebookLM**（现已更名为 **Gemini Notebook**）。你可以创建笔记本，添加网页、YouTube 视频、文本、Google 云端硬盘文件和上传的文件作为来源，提出带引用的问题，运行 Deep Research，并生成所有 Studio 成果：**音频概览**（NotebookLM 播客）、**视频概览**、演示文稿、信息图、报告、数据表、测验、闪卡和思维导图。音频、视频、演示文稿和图片会以 Dify 文件的形式返回。

> 本插件调用 useapi.net 提供的 [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin)，这是第三方 API，并非由 Google 开发，与 Google 无关联，也未获得 Google 认可。使用前需要 useapi.net 订阅（每月 15 美元，包含 useapi.net 的全部 API）以及你自己的 Google 账号。生成使用该 Google 账号自身的 NotebookLM 方案（包括免费方案），useapi.net 不按调用次数收费。

Google 没有为普通 Google 账号提供 NotebookLM API；它唯一的 Gemini Notebook Enterprise API 需要在 Google Cloud 项目中购买企业版许可。本插件使用普通 Google 账号即可。

## 设置

1. **获取 useapi.net API 令牌**：订阅后复制令牌，见 [Setup useapi.net](https://useapi.net/docs/start-here/setup-useapi?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin)。
2. **连接一次 Google 账号**：按照 [Setup Gemini Notebook](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin) 操作，只需用 Google 登录，无需复制 Cookie，也无需 Google Cloud 项目。每个订阅可连接 3 个 Google 账号（最多 100 个），新任务会自动分配到各账号。
3. **安装插件**：在 Dify 插件市场搜索 “NotebookLM”，或在“插件 > 安装插件 > 本地插件包”中上传 [GitHub releases](https://github.com/useapi/notebooklm-api/releases) 里的 `.difypkg`。
4. **授权**：在“工具”中打开 “NotebookLM（Gemini Notebook），由 useapi.net 提供”，点击授权并填写：

| 凭据 | 必填 | 说明 |
|---|:-:|---|
| useapi.net API 令牌 | 是 | 第 1 步获得的令牌，由 Dify 加密保存。 |
| 默认 Google 账号邮箱 | 否 | 工具需要账号时使用哪个已连接的 Google 账号。留空则由 useapi.net 选择最空闲的账号。 |

保存凭据时会调用一次 `GET /accounts` 进行检查，确认令牌有效且至少已连接一个 Google 账号。

### 网络要求

插件只通过 HTTPS 连接 `https://api.useapi.net/v1/gemini-notebook`，令牌放在 `Authorization: Bearer` 请求头中。自托管的 Dify 需要能访问 `api.useapi.net`。

## 工具

共 56 个工具，每个工具对应一项任务，API 的选项以下拉菜单呈现。完整列表及对应接口见英文版 README。

- **账号与任务**：列出 Google 账号、获取账号用量、列出运行中的任务、获取任务状态、取消任务。
- **笔记本**：列出、创建、获取、重命名、删除、复制笔记本，获取笔记本指南，查看与修改共享设置。
- **来源**：添加网址/YouTube/文本/Google 云端硬盘/Play 图书，上传文件，获取、重命名、删除来源，同步云端硬盘来源，追加文本，搜索来源，列出 Play 图书。
- **聊天**：向笔记本提问（带引用）、获取聊天记录、清除聊天、配置聊天风格与长度。
- **研究**：发现来源（快速）或 Deep Research，并导入结果。
- **Studio 成果**：音频概览（播客）、视频概览、演示文稿、信息图、报告、交互式报告、数据表、测验、闪卡、思维导图，以及生成推荐项、重试失败成果、修改单张幻灯片。
- **成果管理**：列出、获取、下载、删除成果，导出到 Google 文档或表格。
- **笔记、标签与合集**：列出/创建/删除笔记、将笔记转为来源，标记来源，列出/创建/更新合集。

所有生成工具既可以使用 `notebook` ID，也可以直接提供 `urls` 和/或 `text`，由工具自动创建笔记本。工具默认最多等待 120 秒，然后返回文本、文件和工作流变量；若任务仍在运行，则返回带 `jobid` 的提示，请用“获取任务状态”（同样每次最多等待 120 秒）继续查询，不要重新生成。在工作流中可将“最长等待”调高到 540 秒，在一个节点内拿到文件。

## 使用示例

### 工作流：一个节点把链接变成播客

```
[开始：urls（段落）]
   -> [NotebookLM > 生成音频概览（播客）]  urls = {{开始.urls}}，格式 = 深入探讨，长度 = 较短，语言 = zh_Hans
   -> [结束：播客 = {{生成音频概览.files}}，摘要 = {{生成音频概览.text}}]
```

### Agent：基于你的笔记本的研究助手

为 Agent 添加“列出笔记本”“获取笔记本”“添加来源”“向笔记本提问”“生成音频概览”“获取任务状态”等工具，并在提示词中要求：只依据“向笔记本提问”的结果作答并保留引用编号；生成音频或视频概览前先征得用户同意，因为会消耗其 Google 用量。

## 等待、限额与错误

- 聊天约 15 至 30 秒；发现来源约 15 秒；Deep Research 3 至 5 分钟；音频概览 3 至 10 分钟；视频概览 10 分钟以上。插件每 15 秒查询一次，默认每次调用最多等待 120 秒（工作流中最多可设 540 秒，低于 Dify 默认的 600 秒插件执行上限）。
- 每个 Google 账号都有 NotebookLM 自己的用量（每 5 小时恢复一次，另有每周用量）。“获取账号用量”可查看剩余额度。
- 错误会以易读的信息返回，例如令牌无效（401）、订阅过期（402）、账号未连接（404）、来源仍在处理（409）、账号繁忙或用量不足及重置时间（429）、账号被 Google 登出（596）。

## 隐私

插件只向 `api.useapi.net` 发送请求，不保存任何数据。详见 [PRIVACY.md](../PRIVACY.md) 和 useapi.net 的[条款与隐私政策](https://useapi.net/docs/legal)。

## 支持

- API 文档：https://useapi.net/docs/api-gemini-notebook-v1
- 中文教程：https://useapi.net/docs/articles/gemini-notebook-api-zh
- 示例代码：https://github.com/useapi/notebooklm-api
- 邮箱 support@useapi.net，或在 [Discord](https://discord.gg/w28uK3cnmF)、[Telegram](https://t.me/use_api) 提问。
