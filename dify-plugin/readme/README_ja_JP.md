# NotebookLM（Gemini Notebook）by useapi.net

**作者：** useapi · **バージョン：** 0.1.1 · **種類：** ツール · **ソース：** https://github.com/useapi/notebooklm-api/tree/main/dify-plugin · **連絡先：** support@useapi.net

Dify のワークフロー、チャットフロー、エージェントから Google Gemini Notebook（旧称 NotebookLM）を使えるプラグインです。ノートブックを作成し、ウェブページ、YouTube 動画、テキスト、Google ドライブのファイル、アップロードしたファイルをソースとして追加し、引用付きで質問に答えさせ、Deep Research を実行し、Studio のすべての出力を生成できます：音声解説（Gemini Notebook のポッドキャスト）、動画解説、スライド資料、インフォグラフィック、レポート、データ表、テスト、フラッシュカード、マインドマップ。音声・動画・スライド・画像は Dify のファイルとして返されます。

> このプラグインは useapi.net の [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin)（サードパーティ API）を呼び出します。Google が開発したものではなく、Google との提携や承認もありません。useapi.net のサブスクリプション（月額 15 ドル、useapi.net のすべての API が対象）と Google アカウントが必要です。生成はそのアカウントの Google AI サブスクリプション（無料プランを含む）で実行され、useapi.net による呼び出しごとの課金はありません。

Google は通常の Google アカウント向けに Gemini Notebook API を提供していません。唯一の Gemini Notebook Enterprise API は、Google Cloud プロジェクトでの Enterprise ライセンスが必要です。このプラグインは通常の Google アカウントで動作します。

## セットアップ

1. **useapi.net の API トークンを取得**：サブスクリプションに登録してトークンをコピーします（[Setup useapi.net](https://useapi.net/docs/start-here/setup-useapi?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin)）。
2. **Google アカウントを一度だけ接続**：[Setup Gemini Notebook](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin) の手順で Google にログインするだけです。Cookie のコピーや Google Cloud プロジェクトは不要です。1 つのサブスクリプションで Google アカウントを 3 つ（最大 100）接続でき、新しいジョブは自動で振り分けられます。
3. **プラグインをインストール**：Dify マーケットプレイスで「NotebookLM」を検索するか、[GitHub releases](https://github.com/useapi/notebooklm-api/releases) の `.difypkg` を「プラグイン > プラグインをインストール > ローカルパッケージファイル」からアップロードします。
4. **認証**：「ツール」で「NotebookLM（Gemini Notebook）by useapi.net」を開き、認証をクリックして入力します：

| 認証情報 | 必須 | 内容 |
|---|:-:|---|
| useapi.net API トークン | はい | 手順 1 のトークン。Dify が暗号化して保存します。 |
| 既定の Google アカウントのメール | いいえ | ツールがアカウントを必要とするときに使う接続済みアカウント。空欄なら useapi.net が最も空いているアカウントを選びます。 |

保存時に `GET /accounts` を 1 回呼び出し、トークンが有効で Google アカウントが 1 つ以上接続されていることを確認します。

### 接続要件

プラグインは HTTPS で `https://api.useapi.net/v1/gemini-notebook` のみに接続し、トークンは `Authorization: Bearer` ヘッダーで送ります。セルフホストの Dify では `api.useapi.net` への外向き HTTPS 通信が必要です。

## ツール

56 個のツールがあり、1 つのツールが 1 つの作業を担当します。API のオプションはドロップダウンで選べます。全ツールと対応するエンドポイントは英語版 README をご覧ください。

- **アカウントとジョブ**：Google アカウント一覧、使用量の取得、実行中のジョブ一覧、ジョブの状態取得、キャンセル。
- **ノートブック**：一覧、作成、取得、名前変更、削除、複製、ノートブックガイド、共有設定の確認と変更。
- **ソース**：URL／YouTube／テキスト／Google ドライブ／Play ブックスの追加、ファイルのアップロード、取得・名前変更・削除、ドライブの同期、テキストの追記、ソース検索、Play ブックス一覧。
- **チャット**：引用付きでノートブックに質問、チャット履歴、チャットの消去、回答スタイルと長さの設定。
- **リサーチ**：ソースを探す（高速）または Deep Research と、その結果のインポート。
- **Studio の出力**：音声解説（ポッドキャスト）、動画解説、スライド資料、インフォグラフィック、レポート、インタラクティブレポート、データ表、テスト、フラッシュカード、マインドマップ、提案アイテムの生成、失敗した生成の再試行、スライド 1 枚の修正。
- **アーティファクト**：一覧、取得、ダウンロード、削除、Google ドキュメント／スプレッドシートへのエクスポート。
- **メモ・ラベル・コレクション**：メモの一覧／作成／削除とソースへの変換、ソースのラベル付け、コレクションの一覧／作成／更新。

生成ツールは `notebook` ID のほか、`urls` や `text` を渡してその場でノートブックを作成することもできます。既定では最大 120 秒待ち、テキスト・ファイル・ワークフロー変数を返します。実行中の場合は `jobid` 付きのメッセージを返すので、生成をやり直さず「ジョブの状態を取得」（こちらも 1 回最大 120 秒待機）で確認してください。ワークフローでは「最大待機時間」を 540 秒まで上げれば、1 つのノードでファイルを受け取れます。

## 使用例

### ワークフロー：1 つのノードでリンクをポッドキャストに

```
[開始：urls（段落）]
   -> [NotebookLM > 音声解説を生成（ポッドキャスト）]  urls = {{開始.urls}}、形式 = ディープダイブ、長さ = 短め、言語 = ja
   -> [終了：podcast = {{音声解説を生成.files}}、summary = {{音声解説を生成.text}}]
```

### エージェント：ノートブックを使うリサーチアシスタント

「ノートブック一覧」「ノートブックを取得」「ソースを追加」「ノートブックに質問」「音声解説を生成」「ジョブの状態を取得」を追加し、指示に「回答は『ノートブックに質問』の結果のみに基づき、引用番号を残す」「音声解説や動画解説は Google の使用量を消費するので、開始前にユーザーに確認する」と書きます。

## 待機・制限・エラー

- チャットは 15〜30 秒、ソースを探すは約 15 秒、Deep Research は 3〜5 分、音声解説は 3〜10 分、動画解説は 10 分以上かかります。プラグインは 15 秒ごとに状態を確認し、既定では 1 回の呼び出しで最大 120 秒待ちます（ワークフローでは最大 540 秒まで設定可能で、Dify 既定のプラグイン実行上限 600 秒未満）。
- 各 Google アカウントには Gemini Notebook 独自の使用量枠（5 時間ごとに回復、さらに週ごとの枠）があります。「アカウントの使用量を取得」で残量を確認できます。
- エラーは読みやすいメッセージで返されます。例：トークンが無効（401）、サブスクリプション切れ（402）、アカウント未接続（404）、ソース処理中（409）、アカウントが混雑中または使用量不足とリセット時刻（429）、Google によるログアウト（596）。

## プライバシー

プラグインは `api.useapi.net` にのみリクエストを送り、データを保存しません。詳細は [PRIVACY.md](../PRIVACY.md) と useapi.net の[利用規約とプライバシーポリシー](https://useapi.net/docs/legal)をご覧ください。

## サポート

- API リファレンス：https://useapi.net/docs/api-gemini-notebook-v1
- サンプルコード：https://github.com/useapi/notebooklm-api
- メール support@useapi.net、または [Discord](https://discord.gg/w28uK3cnmF)／[Telegram](https://t.me/use_api) でお問い合わせください。
