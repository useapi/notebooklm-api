"""Single source of truth for every tool: names, parameters, enums and the
four Dify UI languages (en_US, zh_Hans, ja_JP, pt_BR). `dev/gen_tools.py`
writes tools/*.yaml, tools/*.py and the provider's tool list from this file.

Parameter names, enums and limits follow the public API reference:
https://useapi.net/docs/api-gemini-notebook-v1
LLM-facing descriptions stay in English.
"""

from __future__ import annotations

from typing import Any


def L(en: str, zh: str, ja: str, pt: str) -> dict[str, str]:
    return {"en_US": en, "zh_Hans": zh, "ja_JP": ja, "pt_BR": pt}


def opt(value: str, label: dict[str, str]) -> dict[str, Any]:
    return {"value": value, "label": label}


def param(
    name: str,
    ptype: str,
    label: dict[str, str],
    human: dict[str, str],
    llm: str | None = None,
    *,
    required: bool = False,
    form: str = "llm",
    default: Any = None,
    options: list[dict[str, Any]] | None = None,
    min: int | None = None,
    max: int | None = None,
) -> dict[str, Any]:
    p: dict[str, Any] = {
        "name": name,
        "type": ptype,
        "required": required,
        "label": label,
        "human_description": human,
    }
    if form == "llm":
        p["llm_description"] = llm or human["en_US"]
    p["form"] = form
    if default is not None:
        p["default"] = default
    if options:
        p["options"] = options
    if min is not None:
        p["min"] = min
    if max is not None:
        p["max"] = max
    return p


# ------------------------------------------------------------------ shared parameters

NOTEBOOK_LLM = "The notebook id, e.g. user:12345-user@example.com-notebook:<uuid>, from List notebooks or Create notebook."


def NOTEBOOK(required: bool = True, llm: str = NOTEBOOK_LLM) -> dict[str, Any]:
    return param(
        "notebook",
        "string",
        L("Notebook ID", "笔记本 ID", "ノートブック ID", "ID do notebook"),
        L(
            "The notebook id returned by List notebooks or Create notebook.",
            "由“列出笔记本”或“创建笔记本”返回的笔记本 ID。",
            "「ノートブック一覧」または「ノートブックを作成」で返されるノートブック ID。",
            "O ID do notebook retornado por Listar notebooks ou Criar notebook.",
        ),
        llm,
        required=required,
    )


def EMAIL(purpose_en: str = "the Google account to use") -> dict[str, Any]:
    return param(
        "email",
        "string",
        L("Google account email", "Google 账号邮箱", "Google アカウントのメール", "E-mail da conta Google"),
        L(
            "Optional. A connected Google account. Defaults to the email in the credentials, or the least busy account.",
            "可选。已连接的 Google 账号。默认使用凭据中的邮箱，或最空闲的账号。",
            "任意。接続済みの Google アカウント。省略時は認証情報のメール、または最も空いているアカウントを使います。",
            "Opcional. Uma conta Google conectada. O padrão é o e-mail das credenciais ou a conta menos ocupada.",
        ),
        f"Optional email of {purpose_en}. Leave empty to use the default account.",
    )


def SOURCE_ID(llm: str = "The source id, from Get notebook or Add sources.") -> dict[str, Any]:
    return param(
        "source",
        "string",
        L("Source ID", "来源 ID", "ソース ID", "ID da fonte"),
        L(
            "The source id returned by Add sources or Get notebook.",
            "由“添加来源”或“获取笔记本”返回的来源 ID。",
            "「ソースを追加」または「ノートブックを取得」で返されるソース ID。",
            "O ID da fonte retornado por Adicionar fontes ou Obter notebook.",
        ),
        llm,
        required=True,
    )


SOURCES = param(
    "sources",
    "string",
    L("Source IDs", "来源 ID 列表", "ソース ID 一覧", "IDs das fontes"),
    L(
        "Optional. Limit to these source ids, one per line. Default: every ready source.",
        "可选。仅使用这些来源 ID，每行一个。默认：所有已就绪的来源。",
        "任意。使うソース ID を 1 行に 1 つずつ指定します。省略時は準備完了のすべてのソース。",
        "Opcional. Limita a estes IDs de fonte, um por linha. Padrão: todas as fontes prontas.",
    ),
    "Optional source ids of this notebook, separated by new lines or commas (1 to 300). Leave empty to use every ready source.",
)

ARTIFACT = param(
    "artifact",
    "string",
    L("Artifact ID", "成果 ID", "アーティファクト ID", "ID do artefato"),
    L(
        "The artifact id from a job or from List artifacts.",
        "来自任务或“列出成果”的成果 ID。",
        "ジョブまたは「アーティファクト一覧」のアーティファクト ID。",
        "O ID do artefato vindo de um job ou de Listar artefatos.",
    ),
    "The artifact id, e.g. user:12345-user@example.com-artifact:<notebook uuid>:<artifact uuid>.",
    required=True,
)

JOBID = param(
    "jobid",
    "string",
    L("Job ID", "任务 ID", "ジョブ ID", "ID do job"),
    L(
        "The jobid returned when the generation or research started.",
        "开始生成或研究时返回的任务 ID（jobid）。",
        "生成またはリサーチの開始時に返された jobid。",
        "O jobid retornado quando a geração ou pesquisa começou.",
    ),
    "The jobid, e.g. job:<uuid>-user:12345-user@example.com-bot:gemini_notebook.",
    required=True,
)

CONVERSATION = param(
    "conversation",
    "string",
    L("Conversation ID", "对话 ID", "会話 ID", "ID da conversa"),
    L(
        "Optional. A conversation id from an earlier answer. Default: start a new one (or the latest, when reading).",
        "可选。之前回答返回的对话 ID。默认：新建对话（读取时为最近一次对话）。",
        "任意。以前の回答で返された会話 ID。省略時は新しい会話（読み取り時は最新の会話）。",
        "Opcional. Um ID de conversa de uma resposta anterior. Padrão: nova conversa (ou a mais recente, ao ler).",
    ),
    "Optional conversation id returned by an earlier Ask notebook answer.",
)

WAIT = param(
    "wait",
    "boolean",
    L("Wait for the result", "等待结果", "結果を待つ", "Aguardar o resultado"),
    L(
        "Wait until the job finishes (up to the maximum wait). Off: return the job id at once.",
        "等待任务完成（不超过最长等待时间）。关闭时立即返回任务 ID。",
        "ジョブの完了まで待ちます（最大待機時間まで）。オフにするとすぐにジョブ ID を返します。",
        "Aguarda o job terminar (até o tempo máximo). Desligado: retorna o ID do job na hora.",
    ),
    form="form",
    default=True,
)


def MAX_WAIT(default: int = 120) -> dict[str, Any]:
    return param(
        "max_wait_seconds",
        "number",
        L("Maximum wait (seconds)", "最长等待（秒）", "最大待機時間（秒）", "Espera máxima (segundos)"),
        L(
            f"How long to wait, 10 to 540 seconds (default {default}). A job still running is returned with its job id.",
            f"最长等待时间，10 到 540 秒（默认 {default}）。仍在运行的任务会连同任务 ID 一起返回。",
            f"待機時間は 10〜540 秒（既定 {default}）。実行中のジョブはジョブ ID とともに返されます。",
            f"Quanto esperar, de 10 a 540 segundos (padrão {default}). Um job ainda em execução é retornado com seu ID.",
        ),
        form="form",
        default=default,
        min=10,
        max=540,
    )


RETURN_FILE = param(
    "return_file",
    "boolean",
    L("Attach the file", "附加文件", "ファイルを添付", "Anexar o arquivo"),
    L(
        "Download the finished audio, video, PDF/PPTX or image and return it as a file.",
        "下载生成的音频、视频、PDF/PPTX 或图片，并作为文件返回。",
        "完成した音声・動画・PDF/PPTX・画像をダウンロードしてファイルとして返します。",
        "Baixa o áudio, vídeo, PDF/PPTX ou imagem pronto e retorna como arquivo.",
    ),
    form="form",
    default=True,
)

LANGUAGE = param(
    "language",
    "string",
    L("Output language", "输出语言", "出力言語", "Idioma de saída"),
    L(
        "Optional language code, e.g. en, es, pt_BR, ja, zh_Hans. Default: en.",
        "可选，语言代码，例如 en、es、pt_BR、ja、zh_Hans。默认：en。",
        "任意。言語コード（例：en、es、pt_BR、ja、zh_Hans）。既定は en。",
        "Código de idioma opcional, ex.: en, es, pt_BR, ja, zh_Hans. Padrão: en.",
    ),
    "Optional output language code such as en, es, pt_BR, ja or zh_Hans. Default en.",
)

INSTRUCTIONS = param(
    "instructions",
    "string",
    L("Instructions", "说明", "指示", "Instruções"),
    L(
        "Optional. What to focus on or how to shape the result (up to 10,000 characters).",
        "可选。重点内容或结果的形式（最多 10,000 个字符）。",
        "任意。重点や仕上がりの指示（最大 10,000 文字）。",
        "Opcional. No que focar ou como moldar o resultado (até 10.000 caracteres).",
    ),
    "Optional focus or shaping instructions for the result, up to 10,000 characters.",
)

URLS_ONESHOT = param(
    "urls",
    "string",
    L("Source URLs (one-shot)", "来源网址（一次性）", "ソース URL（ワンショット）", "URLs de fonte (uso único)"),
    L(
        "Used only without a notebook: web pages or YouTube links, one per line. A new notebook is created for them.",
        "仅在未提供笔记本时使用：网页或 YouTube 链接，每行一个。会为其新建一个笔记本。",
        "ノートブック未指定時のみ使用：ウェブページまたは YouTube のリンクを 1 行に 1 つ。新しいノートブックが作成されます。",
        "Usado só sem notebook: páginas web ou links do YouTube, um por linha. Um novo notebook é criado para eles.",
    ),
    "Only when no notebook is given: 1 to 50 web page or YouTube URLs, separated by new lines. A notebook is created for them automatically.",
)

TEXT_ONESHOT = param(
    "text",
    "string",
    L("Source text (one-shot)", "来源文本（一次性）", "ソーステキスト（ワンショット）", "Texto de fonte (uso único)"),
    L(
        "Used only without a notebook: pasted text to generate from (up to 500,000 characters).",
        "仅在未提供笔记本时使用：用于生成的粘贴文本（最多 500,000 个字符）。",
        "ノートブック未指定時のみ使用：生成元の貼り付けテキスト（最大 500,000 文字）。",
        "Usado só sem notebook: texto colado para gerar (até 500.000 caracteres).",
    ),
    "Only when no notebook is given: pasted text to use as a source, up to 500,000 characters.",
)

TITLE_ONESHOT = param(
    "title",
    "string",
    L("Notebook title (one-shot)", "笔记本标题（一次性）", "ノートブックのタイトル（ワンショット）", "Título do notebook (uso único)"),
    L(
        "Used only without a notebook: the title of the notebook created for this request.",
        "仅在未提供笔记本时使用：为本次请求新建的笔记本标题。",
        "ノートブック未指定時のみ使用：このリクエスト用に作成するノートブックのタイトル。",
        "Usado só sem notebook: o título do notebook criado para este pedido.",
    ),
    "Only when no notebook is given: title of the auto-created notebook (up to 200 characters).",
)

DELETE_NOTEBOOK = param(
    "delete_notebook",
    "boolean",
    L("Delete the one-shot notebook", "删除一次性笔记本", "ワンショットのノートブックを削除", "Excluir o notebook de uso único"),
    L(
        "Text results only: delete the auto-created notebook when the job finishes.",
        "仅限文本类结果：任务完成后删除自动创建的笔记本。",
        "テキスト結果のみ：ジョブ完了後に自動作成したノートブックを削除します。",
        "Só para resultados em texto: exclui o notebook criado automaticamente quando o job termina.",
    ),
    form="form",
    default=False,
)

REPLY_URL = param(
    "reply_url",
    "string",
    L("Webhook URL", "Webhook 地址", "Webhook URL", "URL de webhook"),
    L(
        "Optional public URL that receives the finished job record by POST.",
        "可选。接收已完成任务记录（POST）的公开地址。",
        "任意。完了したジョブ記録を POST で受け取る公開 URL。",
        "URL pública opcional que recebe o registro do job finalizado via POST.",
    ),
    form="form",
)

JOB_OUTPUT = {
    "jobid": {"type": "string"},
    "status": {"type": "string"},
    "notebook": {"type": "string"},
    "artifact": {"type": "string"},
    "title": {"type": "string"},
    "text": {"type": "string"},
    "file_urls": {"type": "array", "items": {"type": "string"}},
}

# ------------------------------------------------------------------ option sets

LENGTH_3 = [
    opt("short", L("Short", "较短", "短め", "Curto")),
    opt("default", L("Default", "默认", "標準", "Padrão")),
    opt("long", L("Long", "较长", "長め", "Longo")),
]
QUANTITY = [
    opt("fewer", L("Fewer", "较少", "少なめ", "Menos")),
    opt("standard", L("Standard", "标准", "標準", "Padrão")),
    opt("more", L("More", "较多", "多め", "Mais")),
]
DIFFICULTY = [
    opt("easy", L("Easy", "简单", "易しい", "Fácil")),
    opt("medium", L("Medium", "中等", "普通", "Médio")),
    opt("hard", L("Hard", "困难", "難しい", "Difícil")),
]
INFOGRAPHIC_STYLES = [
    opt("auto", L("Auto", "自动", "自動", "Automático")),
    opt("sketch_note", L("Sketch note", "手绘笔记", "スケッチノート", "Sketchnote")),
    opt("professional", L("Professional", "专业", "プロフェッショナル", "Profissional")),
    opt("bento_grid", L("Bento grid", "便当网格", "ベントーグリッド", "Grade bento")),
    opt("editorial", L("Editorial", "杂志编排", "エディトリアル", "Editorial")),
    opt("instructional", L("Instructional", "教学说明", "解説図", "Instrucional")),
    opt("bricks", L("Bricks", "积木", "ブロック", "Blocos")),
    opt("clay", L("Clay", "黏土", "クレイ", "Massinha")),
    opt("anime", L("Anime", "动漫", "アニメ", "Anime")),
    opt("kawaii", L("Kawaii", "可爱", "かわいい", "Kawaii")),
    opt("scientific", L("Scientific", "科学", "サイエンス", "Científico")),
]
ORIENTATION = [
    opt("landscape", L("Landscape", "横向", "横向き", "Paisagem")),
    opt("portrait", L("Portrait", "纵向", "縦向き", "Retrato")),
    opt("square", L("Square", "方形", "正方形", "Quadrado")),
]
DETAIL = [
    opt("concise", L("Concise", "简洁", "簡潔", "Conciso")),
    opt("standard", L("Standard", "标准", "標準", "Padrão")),
    opt("detailed", L("Detailed", "详细", "詳細", "Detalhado")),
]
SLIDES_FORMAT = [
    opt("detailed", L("Detailed deck", "详细演示文稿", "詳細なスライド", "Apresentação detalhada")),
    opt("presenter", L("Presenter slides", "演讲者幻灯片", "プレゼンター用スライド", "Slides para apresentador")),
]


def select(
    name: str, label: dict[str, str], human: dict[str, str], options: list[dict[str, Any]], llm: str | None = None
) -> dict[str, Any]:
    values = ", ".join(o["value"] for o in options)
    return param(name, "select", label, human, llm or f"{human['en_US']} One of: {values}. Leave empty for the default.", options=options)


FMT_LABEL = L("Format", "格式", "形式", "Formato")
LEN_LABEL = L("Length", "长度", "長さ", "Duração")
STYLE_LABEL = L("Visual style", "视觉风格", "ビジュアルスタイル", "Estilo visual")


def quantity_difficulty() -> list[dict[str, Any]]:
    return [
        select(
            "quantity",
            L("Number of items", "数量", "数", "Quantidade"),
            L(
                "Optional. Fewer, standard (default) or more.",
                "可选。较少、标准（默认）或较多。",
                "任意。少なめ・標準（既定）・多め。",
                "Opcional. Menos, padrão ou mais.",
            ),
            QUANTITY,
        ),
        select(
            "difficulty",
            L("Difficulty", "难度", "難易度", "Dificuldade"),
            L(
                "Optional. Easy, medium (default) or hard.",
                "可选。简单、中等（默认）或困难。",
                "任意。易しい・普通（既定）・難しい。",
                "Opcional. Fácil, médio (padrão) ou difícil.",
            ),
            DIFFICULTY,
        ),
    ]


def generation_tail(file_types: bool, wait_default: int, text_only: bool) -> list[dict[str, Any]]:
    tail = [
        NOTEBOOK(required=False, llm=NOTEBOOK_LLM + " Leave empty and give urls or text instead to create a one-shot notebook."),
        SOURCES,
        URLS_ONESHOT,
        TEXT_ONESHOT,
        TITLE_ONESHOT,
        EMAIL("the Google account for a one-shot request"),
    ]
    if text_only:
        tail.append(DELETE_NOTEBOOK)
    tail += [WAIT, MAX_WAIT(wait_default)]
    if file_types:
        tail.append(RETURN_FILE)
    tail.append(REPLY_URL)
    return tail


def gen_human(en: str, zh: str, ja: str, pt: str) -> dict[str, str]:
    """Generation tools all accept a notebook or one-shot sources; say so in every language."""
    return L(
        en + " Give a notebook id, or URLs/text to create a notebook on the fly.",
        zh + "可提供笔记本 ID，或直接提供网址/文本以自动创建笔记本。",
        ja + "ノートブック ID を指定するか、URL／テキストを渡してその場でノートブックを作成できます。",
        pt + " Informe um ID de notebook, ou URLs/texto para criar um notebook na hora.",
    )


# ------------------------------------------------------------------ tools

TOOLS: list[dict[str, Any]] = []


def tool(
    name: str, label: dict[str, str], human: dict[str, str], llm: str, params: list[dict[str, Any]], output: dict[str, Any] | None = None
) -> None:
    TOOLS.append({"name": name, "label": label, "human": human, "llm": llm, "params": params, "output": output})


# --- accounts and jobs

tool(
    "list_accounts",
    L("List Google accounts", "列出 Google 账号", "Google アカウント一覧", "Listar contas Google"),
    L(
        "List the Google accounts connected to useapi.net, with health, plan and running jobs.",
        "列出已连接到 useapi.net 的 Google 账号，包括状态、方案和正在运行的任务。",
        "useapi.net に接続済みの Google アカウントを、状態・プラン・実行中のジョブとともに一覧表示します。",
        "Lista as contas Google conectadas ao useapi.net, com saúde, plano e jobs em execução.",
    ),
    "List the connected Gemini Notebook (NotebookLM) Google accounts with their health and running jobs.",
    [],
    {"emails": {"type": "array", "items": {"type": "string"}}},
)

tool(
    "get_account",
    L("Get account usage", "获取账号用量", "アカウントの使用量を取得", "Ver uso da conta"),
    L(
        "Live plan, usage windows, reset times and per-action cost estimates of one Google account.",
        "某个 Google 账号的实时方案、用量窗口、重置时间和各操作的成本估算。",
        "Google アカウントの現在のプラン、使用量枠、リセット時刻、操作ごとのコスト見積もり。",
        "Plano, janelas de uso, horários de renovação e custo estimado por ação de uma conta Google, ao vivo.",
    ),
    "Get the live NotebookLM usage of one Google account: plan, 5-hour and weekly windows, reset times, estimated cost per action.",
    [EMAIL("the Google account to read")],
)

tool(
    "list_jobs",
    L("List running jobs", "列出运行中的任务", "実行中のジョブ一覧", "Listar jobs em execução"),
    L(
        "What is running on each Google account right now, with its last known usage.",
        "每个 Google 账号当前正在运行的任务及最近的用量。",
        "各 Google アカウントで現在実行中のジョブと、直近の使用量。",
        "O que está em execução em cada conta Google agora, com o último uso conhecido.",
    ),
    "List the generation and research jobs running now on each Google account.",
    [],
)

tool(
    "get_job",
    L("Get job status", "获取任务状态", "ジョブの状態を取得", "Ver status do job"),
    L(
        "Check a generation or research job, optionally wait for it, and return the result with its files.",
        "查询生成或研究任务，可选择等待完成，并返回结果和文件。",
        "生成またはリサーチのジョブを確認し、必要なら完了まで待って結果とファイルを返します。",
        "Consulta um job de geração ou pesquisa, opcionalmente aguarda e retorna o resultado com os arquivos.",
    ),
    "Get a NotebookLM job by jobid. Returns status; when completed, the result text and the audio/video/slide/image files.",
    [JOBID, WAIT, MAX_WAIT(120), RETURN_FILE],
    JOB_OUTPUT,
)

tool(
    "cancel_job",
    L("Cancel job", "取消任务", "ジョブをキャンセル", "Cancelar job"),
    L(
        "Cancel a running job and free its slot. Google may still finish the artifact.",
        "取消正在运行的任务并释放名额。Google 仍可能完成该成果。",
        "実行中のジョブをキャンセルして枠を空けます。Google 側で生成が完了することもあります。",
        "Cancela um job em execução e libera a vaga. O Google ainda pode concluir o artefato.",
    ),
    "Cancel a running NotebookLM job by jobid.",
    [JOBID],
)

# --- notebooks

tool(
    "list_notebooks",
    L("List notebooks", "列出笔记本", "ノートブック一覧", "Listar notebooks"),
    L(
        "List the notebooks of your Google accounts, with titles, source counts and ids.",
        "列出 Google 账号中的笔记本，包括标题、来源数量和 ID。",
        "Google アカウントのノートブックを、タイトル・ソース数・ID とともに一覧表示します。",
        "Lista os notebooks das suas contas Google, com títulos, número de fontes e IDs.",
    ),
    "List Gemini Notebook (NotebookLM) notebooks with their ids, titles and source counts.",
    [EMAIL("the Google account to list")],
    {"notebook_ids": {"type": "array", "items": {"type": "string"}}},
)

tool(
    "create_notebook",
    L("Create notebook", "创建笔记本", "ノートブックを作成", "Criar notebook"),
    L(
        "Create an empty notebook. Add sources to it next.",
        "创建一个空笔记本，然后再添加来源。",
        "空のノートブックを作成します。次にソースを追加してください。",
        "Cria um notebook vazio. Depois adicione fontes a ele.",
    ),
    "Create an empty NotebookLM notebook and return its id.",
    [
        param(
            "title",
            "string",
            L("Title", "标题", "タイトル", "Título"),
            L(
                "Optional notebook title, up to 200 characters.",
                "可选，笔记本标题，最多 200 个字符。",
                "任意。ノートブックのタイトル（最大 200 文字）。",
                "Título opcional do notebook, até 200 caracteres.",
            ),
            "Optional notebook title, up to 200 characters.",
        ),
        EMAIL("the Google account to create the notebook on"),
    ],
    {"notebook": {"type": "string"}, "email": {"type": "string"}},
)

tool(
    "get_notebook",
    L("Get notebook", "获取笔记本", "ノートブックを取得", "Obter notebook"),
    L(
        "A notebook's sources with their processing status, and its Studio artifacts.",
        "笔记本的来源及其处理状态，以及其 Studio 成果。",
        "ノートブックのソースと処理状態、Studio のアーティファクト。",
        "As fontes de um notebook com o status de processamento, e seus artefatos do Studio.",
    ),
    "Get a NotebookLM notebook: every source with its status (preparing, processing, ready, error) and every artifact.",
    [NOTEBOOK()],
    {"source_ids": {"type": "array", "items": {"type": "string"}}, "ready": {"type": "boolean"}},
)

tool(
    "rename_notebook",
    L("Rename notebook", "重命名笔记本", "ノートブック名を変更", "Renomear notebook"),
    L("Change a notebook's title.", "修改笔记本标题。", "ノートブックのタイトルを変更します。", "Altera o título de um notebook."),
    "Rename a NotebookLM notebook.",
    [
        NOTEBOOK(),
        param(
            "title",
            "string",
            L("New title", "新标题", "新しいタイトル", "Novo título"),
            L("1 to 200 characters.", "1 到 200 个字符。", "1〜200 文字。", "De 1 a 200 caracteres."),
            "The new title, 1 to 200 characters.",
            required=True,
        ),
    ],
)

tool(
    "delete_notebook",
    L("Delete notebook", "删除笔记本", "ノートブックを削除", "Excluir notebook"),
    L(
        "Delete a notebook with its sources and artifacts. This cannot be undone.",
        "删除笔记本及其来源和成果，无法撤销。",
        "ノートブックをソースとアーティファクトごと削除します。元に戻せません。",
        "Exclui um notebook com suas fontes e artefatos. Não pode ser desfeito.",
    ),
    "Permanently delete a NotebookLM notebook. Only do this when the user explicitly asks.",
    [NOTEBOOK()],
)

tool(
    "copy_notebook",
    L("Copy notebook", "复制笔记本", "ノートブックを複製", "Copiar notebook"),
    L(
        "Copy a notebook with its sources on the same account.",
        "在同一账号中复制笔记本及其来源。",
        "同じアカウント内でノートブックをソースごと複製します。",
        "Copia um notebook com suas fontes na mesma conta.",
    ),
    "Copy a NotebookLM notebook with its sources.",
    [
        NOTEBOOK(),
        param(
            "title",
            "string",
            L("Title of the copy", "副本标题", "複製のタイトル", "Título da cópia"),
            L("Optional.", "可选。", "任意。", "Opcional."),
            "Optional title of the copy.",
        ),
    ],
    {"notebook": {"type": "string"}},
)

tool(
    "get_notebook_guide",
    L("Get notebook guide", "获取笔记本指南", "ノートブックガイドを取得", "Obter guia do notebook"),
    L(
        "Google's summary of all sources, plus suggested questions and reports.",
        "Google 对所有来源的摘要，以及推荐的问题和报告。",
        "全ソースに対する Google の要約と、おすすめの質問・レポート。",
        "O resumo do Google de todas as fontes, com perguntas e relatórios sugeridos.",
    ),
    "Get the NotebookLM notebook guide: a Markdown summary of the sources, suggested questions and suggested report prompts.",
    [NOTEBOOK()],
    {"summary": {"type": "string"}},
)

tool(
    "get_sharing",
    L("Get sharing settings", "获取共享设置", "共有設定を取得", "Ver compartilhamento"),
    L(
        "Who a notebook is shared with and whether its link is public.",
        "笔记本与谁共享，以及链接是否公开。",
        "ノートブックの共有相手とリンクが公開かどうか。",
        "Com quem o notebook é compartilhado e se o link é público.",
    ),
    "Get the sharing settings of a NotebookLM notebook.",
    [NOTEBOOK()],
)

tool(
    "share_notebook",
    L("Share notebook", "共享笔记本", "ノートブックを共有", "Compartilhar notebook"),
    L(
        "Share a notebook with people, or open it to anyone with the link.",
        "与他人共享笔记本，或设为知道链接的任何人均可访问。",
        "ノートブックをユーザーと共有するか、リンクを知っている全員に公開します。",
        "Compartilha um notebook com pessoas, ou abre para qualquer pessoa com o link.",
    ),
    "Share a NotebookLM notebook with people (viewer or editor), or set link access to public or restricted.",
    [
        NOTEBOOK(),
        param(
            "people_emails",
            "string",
            L("People (emails)", "共享对象（邮箱）", "共有相手（メール）", "Pessoas (e-mails)"),
            L(
                "Optional. Email addresses, one per line (1 to 50).",
                "可选。邮箱地址，每行一个（1 到 50 个）。",
                "任意。メールアドレスを 1 行に 1 つ（1〜50 件）。",
                "Opcional. E-mails, um por linha (1 a 50).",
            ),
            "Optional email addresses to share with, separated by new lines or commas.",
        ),
        select(
            "role",
            L("Role", "角色", "役割", "Papel"),
            L(
                "Role for the people above: viewer (default), editor or remove.",
                "上述对象的角色：查看者（默认）、编辑者或移除。",
                "上記の相手の役割：閲覧者（既定）・編集者・削除。",
                "Papel das pessoas acima: leitor (padrão), editor ou remover.",
            ),
            [
                opt("viewer", L("Viewer", "查看者", "閲覧者", "Leitor")),
                opt("editor", L("Editor", "编辑者", "編集者", "Editor")),
                opt("remove", L("Remove access", "移除访问权限", "アクセスを削除", "Remover acesso")),
            ],
        ),
        select(
            "link",
            L("Link access", "链接访问", "リンクのアクセス", "Acesso pelo link"),
            L(
                "Optional. Public: anyone with the link. Restricted: only the people listed.",
                "可选。公开：知道链接的任何人。受限：仅限列出的人。",
                "任意。公開：リンクを知っている全員。制限付き：登録した人のみ。",
                "Opcional. Público: qualquer pessoa com o link. Restrito: só as pessoas listadas.",
            ),
            [
                opt("public", L("Anyone with the link", "知道链接的任何人", "リンクを知っている全員", "Qualquer pessoa com o link")),
                opt("restricted", L("Restricted", "受限", "制限付き", "Restrito")),
            ],
        ),
        param(
            "allow_copies",
            "boolean",
            L("Allow copies", "允许复制", "コピーを許可", "Permitir cópias"),
            L(
                "Public link only: whether people may copy the notebook.",
                "仅限公开链接：是否允许他人复制笔记本。",
                "公開リンクのみ：ノートブックのコピーを許可するか。",
                "Só link público: se as pessoas podem copiar o notebook.",
            ),
            "Public link only: whether people with the link may copy the notebook.",
        ),
        param(
            "notify",
            "boolean",
            L("Send share email", "发送共享邮件", "共有メールを送信", "Enviar e-mail"),
            L(
                "Off skips Google's share email. Default on.",
                "关闭则不发送 Google 的共享邮件。默认开启。",
                "オフにすると Google の共有メールを送りません。既定はオン。",
                "Desligado não envia o e-mail do Google. Padrão: ligado.",
            ),
            form="form",
            default=True,
        ),
        select(
            "view_level",
            L("What viewers see", "查看者可见内容", "閲覧者に表示する内容", "O que os leitores veem"),
            L(
                "Optional, paid Google plans only: the full notebook or chat only.",
                "可选，仅限 Google 付费方案：完整笔记本或仅聊天。",
                "任意（Google 有料プランのみ）：ノートブック全体かチャットのみ。",
                "Opcional, só planos pagos do Google: notebook completo ou só o chat.",
            ),
            [
                opt("full", L("Full notebook", "完整笔记本", "ノートブック全体", "Notebook completo")),
                opt("chat", L("Chat only", "仅聊天", "チャットのみ", "Somente chat")),
            ],
        ),
    ],
)

# --- sources

WAIT_READY = param(
    "wait_until_ready",
    "boolean",
    L("Wait until ready", "等待就绪", "準備完了まで待つ", "Aguardar ficar pronta"),
    L(
        "Wait until Google has processed the new sources. Chat and Studio use only ready sources.",
        "等待 Google 处理完新来源。聊天和 Studio 只使用已就绪的来源。",
        "Google が新しいソースを処理し終えるまで待ちます。チャットと Studio は準備完了のソースのみ使います。",
        "Aguarda o Google processar as novas fontes. Chat e Studio usam só fontes prontas.",
    ),
    form="form",
    default=True,
)
SOURCE_OUTPUT = {"source_ids": {"type": "array", "items": {"type": "string"}}, "ready": {"type": "boolean"}}

tool(
    "add_sources",
    L("Add sources", "添加来源", "ソースを追加", "Adicionar fontes"),
    L(
        "Add web pages, YouTube videos, pasted text, Google Drive files or Play Books to a notebook.",
        "向笔记本添加网页、YouTube 视频、粘贴文本、Google 云端硬盘文件或 Play 图书。",
        "ノートブックにウェブページ、YouTube 動画、貼り付けテキスト、Google ドライブのファイル、Play ブックスを追加します。",
        "Adiciona páginas web, vídeos do YouTube, texto colado, arquivos do Google Drive ou livros do Play Livros a um notebook.",
    ),
    "Add sources to a NotebookLM notebook: web page and YouTube URLs, pasted text, Google Drive files or Google Play Books. YouTube links become YouTube sources.",
    [
        NOTEBOOK(),
        param(
            "urls",
            "string",
            L("URLs", "网址", "URL", "URLs"),
            L(
                "Web pages or YouTube links, one per line (1 to 50).",
                "网页或 YouTube 链接，每行一个（1 到 50 个）。",
                "ウェブページまたは YouTube のリンクを 1 行に 1 つ（1〜50 件）。",
                "Páginas web ou links do YouTube, um por linha (1 a 50).",
            ),
            "1 to 50 http(s) URLs separated by new lines. youtube.com and youtu.be links are added as YouTube sources.",
        ),
        param(
            "text",
            "string",
            L("Text", "文本", "テキスト", "Texto"),
            L(
                "Optional pasted text, added as one source (up to 500,000 characters).",
                "可选，粘贴的文本，作为一个来源添加（最多 500,000 个字符）。",
                "任意。貼り付けテキストを 1 つのソースとして追加（最大 500,000 文字）。",
                "Texto colado opcional, adicionado como uma fonte (até 500.000 caracteres).",
            ),
            "Optional pasted text added as one source, up to 500,000 characters.",
        ),
        param(
            "title",
            "string",
            L("Text title", "文本标题", "テキストのタイトル", "Título do texto"),
            L(
                "Optional title of the text source. Default: Pasted text.",
                "可选，文本来源的标题。默认：Pasted text。",
                "任意。テキストソースのタイトル。既定は Pasted text。",
                "Título opcional da fonte de texto. Padrão: Pasted text.",
            ),
            "Optional title of the text source, up to 200 characters.",
        ),
        param(
            "drive_files",
            "string",
            L(
                "Google Drive files (JSON)",
                "Google 云端硬盘文件（JSON）",
                "Google ドライブのファイル（JSON）",
                "Arquivos do Google Drive (JSON)",
            ),
            L(
                'Optional JSON array of {"fileId", "mimeType", "name"}.',
                '可选，{"fileId", "mimeType", "name"} 组成的 JSON 数组。',
                '任意。{"fileId", "mimeType", "name"} の JSON 配列。',
                'Array JSON opcional de {"fileId", "mimeType", "name"}.',
            ),
            'Optional JSON array of Google Drive files: [{"fileId": "...", "mimeType": "application/vnd.google-apps.document", "name": "..."}]. Use the exact MIME type.',
        ),
        param(
            "book_ids",
            "string",
            L("Play Books ids", "Play 图书 ID", "Play ブックス ID", "IDs do Play Livros"),
            L(
                "Optional ids from List Play Books, one per line (1 to 20).",
                "可选，来自“列出 Play 图书”的 ID，每行一个（1 到 20 个）。",
                "任意。「Play ブックス一覧」の ID を 1 行に 1 つ（1〜20 件）。",
                "IDs opcionais de Listar Play Livros, um por linha (1 a 20).",
            ),
            "Optional Google Play Books ids from List Play Books.",
        ),
        WAIT_READY,
        MAX_WAIT(120),
    ],
    SOURCE_OUTPUT,
)

tool(
    "upload_source",
    L("Upload file as source", "上传文件作为来源", "ファイルをソースとしてアップロード", "Enviar arquivo como fonte"),
    L(
        "Upload a PDF, Word, PowerPoint, EPUB, Markdown, text, CSV, audio, video or image file to a notebook.",
        "将 PDF、Word、PowerPoint、EPUB、Markdown、文本、CSV、音频、视频或图片文件上传到笔记本。",
        "PDF、Word、PowerPoint、EPUB、Markdown、テキスト、CSV、音声、動画、画像ファイルをノートブックにアップロードします。",
        "Envia um arquivo PDF, Word, PowerPoint, EPUB, Markdown, texto, CSV, áudio, vídeo ou imagem para um notebook.",
    ),
    "Upload a file to a NotebookLM notebook as a source (up to 200 MB). Audio and video are transcribed by Google.",
    [
        NOTEBOOK(),
        param(
            "file",
            "file",
            L("File", "文件", "ファイル", "Arquivo"),
            L("The file to upload.", "要上传的文件。", "アップロードするファイル。", "O arquivo a enviar."),
            "The file to upload.",
            required=True,
        ),
        param(
            "name",
            "string",
            L("File name", "文件名", "ファイル名", "Nome do arquivo"),
            L(
                "Optional name with extension, used as the source title.",
                "可选，含扩展名的文件名，用作来源标题。",
                "任意。拡張子付きのファイル名（ソースのタイトルになります）。",
                "Nome opcional com extensão, usado como título da fonte.",
            ),
            "Optional file name with extension, e.g. report.pdf.",
        ),
        WAIT_READY,
        MAX_WAIT(120),
    ],
    SOURCE_OUTPUT,
)

tool(
    "get_source",
    L("Get source", "获取来源", "ソースを取得", "Obter fonte"),
    L(
        "A source's status and details, optionally with its indexed text.",
        "来源的状态和详情，可选包含其索引文本。",
        "ソースの状態と詳細。必要ならインデックス済みのテキストも返します。",
        "Status e detalhes de uma fonte, opcionalmente com o texto indexado.",
    ),
    "Get one NotebookLM source; with include_content it also returns the full indexed text.",
    [
        SOURCE_ID(),
        param(
            "include_content",
            "boolean",
            L("Include text", "包含文本", "テキストを含める", "Incluir texto"),
            L(
                "Return the source's indexed text.",
                "返回来源的索引文本。",
                "ソースのインデックス済みテキストを返します。",
                "Retorna o texto indexado da fonte.",
            ),
            "true to include the source's full indexed text.",
            default=False,
        ),
    ],
    {"status": {"type": "string"}, "content": {"type": "string"}},
)

tool(
    "rename_source",
    L("Rename source", "重命名来源", "ソース名を変更", "Renomear fonte"),
    L("Change a source's title.", "修改来源标题。", "ソースのタイトルを変更します。", "Altera o título de uma fonte."),
    "Rename a NotebookLM source.",
    [
        SOURCE_ID(),
        param(
            "title",
            "string",
            L("New title", "新标题", "新しいタイトル", "Novo título"),
            L("The new title.", "新标题。", "新しいタイトル。", "O novo título."),
            "The new source title.",
            required=True,
        ),
    ],
)

tool(
    "delete_source",
    L("Delete source", "删除来源", "ソースを削除", "Excluir fonte"),
    L(
        "Remove a source from its notebook.",
        "从笔记本中移除来源。",
        "ノートブックからソースを削除します。",
        "Remove uma fonte do notebook.",
    ),
    "Delete a NotebookLM source. Only when the user asks.",
    [SOURCE_ID()],
)

tool(
    "sync_drive_source",
    L("Sync Google Drive source", "同步 Google 云端硬盘来源", "Google ドライブのソースを同期", "Sincronizar fonte do Drive"),
    L(
        "Re-import a Google Drive source after the file changed.",
        "文件变更后重新导入 Google 云端硬盘来源。",
        "ファイル更新後に Google ドライブのソースを再インポートします。",
        "Reimporta uma fonte do Google Drive depois que o arquivo mudou.",
    ),
    "Re-import a Google Drive source from its current file.",
    [SOURCE_ID("The id of a Google Drive source.")],
)

tool(
    "append_to_source",
    L("Append text to source", "向来源追加文本", "ソースにテキストを追記", "Acrescentar texto à fonte"),
    L(
        "Add more text to an existing source.",
        "向已有来源追加更多文本。",
        "既存のソースにテキストを追記します。",
        "Acrescenta mais texto a uma fonte existente.",
    ),
    "Append text (up to 500,000 characters) to an existing NotebookLM source.",
    [
        SOURCE_ID(),
        param(
            "text",
            "string",
            L("Text", "文本", "テキスト", "Texto"),
            L(
                "The text to add (up to 500,000 characters).",
                "要追加的文本（最多 500,000 个字符）。",
                "追記するテキスト（最大 500,000 文字）。",
                "O texto a acrescentar (até 500.000 caracteres).",
            ),
            "The text to append.",
            required=True,
        ),
        param(
            "title",
            "string",
            L("Heading", "小标题", "見出し", "Cabeçalho"),
            L(
                "Optional heading for the added text.",
                "可选，追加文本的小标题。",
                "任意。追記するテキストの見出し。",
                "Cabeçalho opcional para o texto acrescentado.",
            ),
            "Optional heading for the appended text, up to 200 characters.",
        ),
    ],
)

tool(
    "search_sources",
    L("Search sources", "搜索来源", "ソースを検索", "Pesquisar nas fontes"),
    L(
        "Find the passages of a notebook's sources that match a query.",
        "在笔记本的来源中查找与查询匹配的段落。",
        "ノートブックのソースから、クエリに合う箇所を探します。",
        "Encontra os trechos das fontes de um notebook que correspondem a uma consulta.",
    ),
    "Search a NotebookLM notebook's sources and return matching passages (no AI answer; use Ask notebook for that).",
    [
        NOTEBOOK(),
        param(
            "query",
            "string",
            L("Query", "查询", "検索語", "Consulta"),
            L(
                "What to look for (up to 2,000 characters).",
                "要查找的内容（最多 2,000 个字符）。",
                "探す内容（最大 2,000 文字）。",
                "O que procurar (até 2.000 caracteres).",
            ),
            "What to look for, up to 2,000 characters.",
            required=True,
        ),
        SOURCES,
        param(
            "limit",
            "number",
            L("Max passages", "最多段落数", "最大件数", "Máximo de trechos"),
            L("1 to 100, default 20.", "1 到 100，默认 20。", "1〜100、既定 20。", "De 1 a 100, padrão 20."),
            "Maximum passages, 1 to 100 (default 20).",
            min=1,
            max=100,
        ),
    ],
    {"passages": {"type": "array", "items": {"type": "string"}}},
)

tool(
    "list_play_books",
    L("List Play Books", "列出 Play 图书", "Play ブックス一覧", "Listar Play Livros"),
    L(
        "The ebooks in the account's Google Play Books library that can be added as sources.",
        "账号 Google Play 图书库中可作为来源添加的电子书。",
        "アカウントの Google Play ブックスにある、ソースとして追加できる電子書籍。",
        "Os e-books da biblioteca do Google Play Livros da conta que podem virar fontes.",
    ),
    "List the Google Play Books ebooks of an account, with whether each can be added as a source.",
    [EMAIL("the Google account whose library to list")],
)

# --- chat

tool(
    "ask_notebook",
    L("Ask notebook (cited chat)", "向笔记本提问（带引用）", "ノートブックに質問（引用付き）", "Perguntar ao notebook (com citações)"),
    L(
        "Ask a question answered only from the notebook's sources, with numbered citations.",
        "提出问题，仅依据笔记本的来源作答，并附带编号引用。",
        "ノートブックのソースだけを根拠に、番号付きの引用とともに回答します。",
        "Faz uma pergunta respondida só com as fontes do notebook, com citações numeradas.",
    ),
    "Ask NotebookLM a question about a notebook. The answer is Markdown grounded in the sources with citation markers like [1]; pass the returned conversation id for follow-ups. Takes 15 to 30 seconds.",
    [
        NOTEBOOK(),
        param(
            "question",
            "string",
            L("Question", "问题", "質問", "Pergunta"),
            L("1 to 10,000 characters.", "1 到 10,000 个字符。", "1〜10,000 文字。", "De 1 a 10.000 caracteres."),
            "The question, 1 to 10,000 characters.",
            required=True,
        ),
        CONVERSATION,
        SOURCES,
    ],
    {"answer": {"type": "string"}, "conversation": {"type": "string"}, "citations": {"type": "array", "items": {"type": "object"}}},
)

tool(
    "get_chat_history",
    L("Get chat history", "获取聊天记录", "チャット履歴を取得", "Ver histórico do chat"),
    L("Read back a notebook conversation.", "读取笔记本的对话记录。", "ノートブックの会話を読み込みます。", "Lê uma conversa do notebook."),
    "Get the turns of a NotebookLM chat conversation.",
    [NOTEBOOK(), CONVERSATION],
)

tool(
    "clear_chat",
    L("Clear chat", "清除聊天", "チャットを消去", "Limpar chat"),
    L("Clear a notebook conversation.", "清除笔记本的对话。", "ノートブックの会話を消去します。", "Limpa uma conversa do notebook."),
    "Clear a NotebookLM chat conversation (default: the latest).",
    [NOTEBOOK(), CONVERSATION],
)

tool(
    "configure_chat",
    L("Configure chat", "配置聊天", "チャットを設定", "Configurar chat"),
    L(
        "Set the notebook's answer style (default, learning guide or a custom persona) and length.",
        "设置笔记本的回答风格（默认、学习指南或自定义角色）和长度。",
        "ノートブックの回答スタイル（標準、学習ガイド、カスタムのペルソナ）と長さを設定します。",
        "Define o estilo das respostas do notebook (padrão, guia de aprendizado ou persona personalizada) e o tamanho.",
    ),
    "Configure NotebookLM chat for a notebook: goal (default, learning_guide, custom), a custom persona prompt, and answer length (default, longer, shorter).",
    [
        NOTEBOOK(),
        select(
            "goal",
            L("Conversation style", "对话风格", "会話スタイル", "Estilo da conversa"),
            L(
                "Default, learning guide, or custom (with a persona).",
                "默认、学习指南或自定义（需填写角色）。",
                "標準・学習ガイド・カスタム（ペルソナを指定）。",
                "Padrão, guia de aprendizado ou personalizado (com persona).",
            ),
            [
                opt("default", L("Default", "默认", "標準", "Padrão")),
                opt("learning_guide", L("Learning guide", "学习指南", "学習ガイド", "Guia de aprendizado")),
                opt("custom", L("Custom", "自定义", "カスタム", "Personalizado")),
            ],
        ),
        param(
            "persona",
            "string",
            L("Custom persona", "自定义角色", "カスタムのペルソナ", "Persona personalizada"),
            L(
                "Role, tone or rules for the chat (sets the style to custom).",
                "聊天的角色、语气或规则（会将风格设为自定义）。",
                "チャットの役割・口調・ルール（スタイルはカスタムになります）。",
                "Papel, tom ou regras do chat (define o estilo como personalizado).",
            ),
            "Optional persona prompt (1 to 10,000 characters). Sending it sets goal to custom.",
        ),
        select(
            "length",
            L("Answer length", "回答长度", "回答の長さ", "Tamanho da resposta"),
            L("Default, longer or shorter.", "默认、更长或更短。", "標準・長め・短め。", "Padrão, mais longa ou mais curta."),
            [
                opt("default", L("Default", "默认", "標準", "Padrão")),
                opt("longer", L("Longer", "更长", "長め", "Mais longa")),
                opt("shorter", L("Shorter", "更短", "短め", "Mais curta")),
            ],
        ),
    ],
)

# --- research

tool(
    "research",
    L(
        "Research (Discover sources / Deep Research)",
        "研究（发现来源 / Deep Research）",
        "リサーチ（ソースを探す / Deep Research）",
        "Pesquisa (Descobrir fontes / Deep Research)",
    ),
    L(
        "Let Google find web sources for a question, or write a Deep Research report. Import the results next.",
        "让 Google 为问题查找网络来源，或撰写 Deep Research 报告，然后导入结果。",
        "質問に合うウェブソースを Google に探させるか、Deep Research レポートを作成させます。結果は次にインポートします。",
        "Deixa o Google encontrar fontes na web para uma pergunta, ou escrever um relatório Deep Research. Depois importe os resultados.",
    ),
    "Run NotebookLM research on a notebook. type fast (Discover sources, ~15 s) returns web sources; type deep (Deep Research, 3 to 5 minutes) also writes a Markdown report. Sources are not added until you call Import research results.",
    [
        NOTEBOOK(),
        param(
            "query",
            "string",
            L("Question", "问题", "質問", "Pergunta"),
            L(
                "What to research (1 to 2,000 characters).",
                "研究的内容（1 到 2,000 个字符）。",
                "調べる内容（1〜2,000 文字）。",
                "O que pesquisar (1 a 2.000 caracteres).",
            ),
            "What to research, 1 to 2,000 characters.",
            required=True,
        ),
        select(
            "type",
            L("Research type", "研究类型", "リサーチの種類", "Tipo de pesquisa"),
            L(
                "Fast: Discover sources (default). Deep: Deep Research report.",
                "快速：发现来源（默认）。深度：Deep Research 报告。",
                "高速：ソースを探す（既定）。詳細：Deep Research レポート。",
                "Rápida: Descobrir fontes (padrão). Profunda: relatório Deep Research.",
            ),
            [
                opt("fast", L("Fast (Discover sources)", "快速（发现来源）", "高速（ソースを探す）", "Rápida (Descobrir fontes)")),
                opt("deep", L("Deep Research", "Deep Research（深度研究）", "Deep Research（詳細リサーチ）", "Deep Research (profunda)")),
            ],
        ),
        select(
            "source",
            L("Search in", "搜索范围", "検索先", "Pesquisar em"),
            L(
                "Web (default) or the account's Google Drive (fast only).",
                "网络（默认）或账号的 Google 云端硬盘（仅限快速）。",
                "ウェブ（既定）またはアカウントの Google ドライブ（高速のみ）。",
                "Web (padrão) ou o Google Drive da conta (só rápida).",
            ),
            [
                opt("web", L("Web", "网络", "ウェブ", "Web")),
                opt("drive", L("Google Drive", "Google 云端硬盘", "Google ドライブ", "Google Drive")),
            ],
        ),
        WAIT,
        MAX_WAIT(120),
        REPLY_URL,
    ],
    JOB_OUTPUT,
)

tool(
    "import_research",
    L("Import research results", "导入研究结果", "リサーチ結果をインポート", "Importar resultados da pesquisa"),
    L(
        "Add the sources found by a research job (and the Deep Research report) to its notebook.",
        "将研究任务找到的来源（以及 Deep Research 报告）添加到其笔记本。",
        "リサーチジョブで見つかったソース（と Deep Research レポート）をノートブックに追加します。",
        "Adiciona ao notebook as fontes encontradas por um job de pesquisa (e o relatório Deep Research).",
    ),
    "Import the results of a completed NotebookLM research job into its notebook. Default: every cited source, plus the report for Deep Research.",
    [
        JOBID,
        param(
            "urls",
            "string",
            L("URLs to import", "要导入的网址", "インポートする URL", "URLs a importar"),
            L(
                "Optional subset of the found URLs, one per line. Default: every cited source.",
                "可选，找到的网址中的一部分，每行一个。默认：所有被引用的来源。",
                "任意。見つかった URL のうち取り込むものを 1 行に 1 つ。既定は引用されたすべてのソース。",
                "Subconjunto opcional das URLs encontradas, uma por linha. Padrão: todas as fontes citadas.",
            ),
            "Optional URLs from the job's result.sources, separated by new lines. Leave empty to import every cited source.",
        ),
        param(
            "include_report",
            "boolean",
            L("Import the report", "导入报告", "レポートをインポート", "Importar o relatório"),
            L(
                "Add the Deep Research report as a source. Default: yes when no URLs are given.",
                "将 Deep Research 报告作为来源添加。默认：未指定网址时为是。",
                "Deep Research レポートをソースとして追加します。既定：URL 未指定時はオン。",
                "Adiciona o relatório Deep Research como fonte. Padrão: sim quando nenhuma URL é dada.",
            ),
            "Whether to import the Deep Research report as a source.",
        ),
    ],
    {"source_ids": {"type": "array", "items": {"type": "string"}}},
)

# --- Studio generation

tool(
    "generate_audio_overview",
    L(
        "Generate Audio Overview (podcast)",
        "生成音频概览（播客）",
        "音声解説を生成（ポッドキャスト）",
        "Gerar Visão geral em áudio (podcast)",
    ),
    gen_human(
        "The Gemini Notebook (NotebookLM) podcast: two AI hosts discuss your sources. Returns an .m4a file.",
        "Gemini Notebook（NotebookLM）播客：两位 AI 主持人讨论你的来源，返回 .m4a 文件。",
        "Gemini Notebook（NotebookLM）のポッドキャスト：2 人の AI ホストがソースについて語り合います。.m4a ファイルを返します。",
        "O podcast do Gemini Notebook (NotebookLM): dois apresentadores de IA discutem suas fontes. Retorna um arquivo .m4a.",
    ),
    "Generate a NotebookLM Audio Overview (podcast) from a notebook, or from urls/text in one shot. Takes about 3 to 10 minutes; returns the .m4a file when finished, or the jobid to check later with Get job status.",
    [
        select(
            "format",
            FMT_LABEL,
            L(
                "Deep dive (default), brief, critique or debate.",
                "深入探讨（默认）、简要、评论或辩论。",
                "ディープダイブ（既定）・概要・批評・ディベート。",
                "Análise aprofundada (padrão), resumo, crítica ou debate.",
            ),
            [
                opt("deep_dive", L("Deep dive", "深入探讨", "ディープダイブ", "Análise aprofundada")),
                opt("brief", L("Brief", "简要", "概要", "Resumo")),
                opt("critique", L("Critique", "评论", "批評", "Crítica")),
                opt("debate", L("Debate", "辩论", "ディベート", "Debate")),
            ],
        ),
        select(
            "length",
            LEN_LABEL,
            L("Short, default or long.", "较短、默认或较长。", "短め・標準・長め。", "Curto, padrão ou longo."),
            LENGTH_3,
        ),
        LANGUAGE,
        INSTRUCTIONS,
        *generation_tail(True, 120, False),
    ],
    JOB_OUTPUT,
)

tool(
    "generate_video_overview",
    L("Generate Video Overview", "生成视频概览", "動画解説を生成", "Gerar Visão geral em vídeo"),
    gen_human(
        "A narrated video about your sources. Returns an .mp4 file.",
        "关于来源的解说视频，返回 .mp4 文件。",
        "ソースについてのナレーション付き動画。.mp4 ファイルを返します。",
        "Um vídeo narrado sobre suas fontes. Retorna um arquivo .mp4.",
    ),
    "Generate a NotebookLM Video Overview. Usually takes 10 minutes or more, so expect a jobid to check later with Get job status.",
    [
        select(
            "format",
            FMT_LABEL,
            L(
                "Explainer (default), brief, cinematic or short.",
                "讲解（默认）、简要、电影感或短视频。",
                "解説（既定）・概要・シネマティック・ショート。",
                "Explicativo (padrão), resumo, cinematográfico ou curto.",
            ),
            [
                opt("explainer", L("Explainer", "讲解", "解説", "Explicativo")),
                opt("brief", L("Brief", "简要", "概要", "Resumo")),
                opt("cinematic", L("Cinematic", "电影感", "シネマティック", "Cinematográfico")),
                opt("short", L("Short", "短视频", "ショート", "Curto")),
            ],
        ),
        select(
            "style",
            STYLE_LABEL,
            L(
                "Explainer and brief only. Default: auto.",
                "仅限讲解和简要格式。默认：自动。",
                "解説と概要のみ。既定は自動。",
                "Só explicativo e resumo. Padrão: automático.",
            ),
            [
                opt("auto", L("Auto", "自动", "自動", "Automático")),
                opt("classic", L("Classic", "经典", "クラシック", "Clássico")),
                opt("whiteboard", L("Whiteboard", "白板", "ホワイトボード", "Quadro branco")),
                opt("heritage", L("Heritage", "传统", "ヘリテージ", "Tradicional")),
                opt("paper_craft", L("Paper craft", "纸艺", "ペーパークラフト", "Papercraft")),
                opt("watercolor", L("Watercolor", "水彩", "水彩", "Aquarela")),
                opt("anime", L("Anime", "动漫", "アニメ", "Anime")),
                opt("retro_print", L("Retro print", "复古印刷", "レトロプリント", "Impressão retrô")),
                opt("kawaii", L("Kawaii", "可爱", "かわいい", "Kawaii")),
                opt(
                    "custom",
                    L("Custom (style prompt)", "自定义（风格提示）", "カスタム（スタイル指定）", "Personalizado (prompt de estilo)"),
                ),
            ],
        ),
        param(
            "style_prompt",
            "string",
            L("Style prompt", "风格提示", "スタイルの指示", "Prompt de estilo"),
            L(
                "Your own visual style (up to 2,000 characters). Sets the style to custom.",
                "自定义视觉风格（最多 2,000 个字符），会将风格设为自定义。",
                "独自のビジュアルスタイル（最大 2,000 文字）。スタイルはカスタムになります。",
                "Seu próprio estilo visual (até 2.000 caracteres). Define o estilo como personalizado.",
            ),
            "Optional custom visual style description, up to 2,000 characters; implies style custom.",
        ),
        LANGUAGE,
        INSTRUCTIONS,
        *generation_tail(True, 120, False),
    ],
    JOB_OUTPUT,
)

tool(
    "generate_slide_deck",
    L("Generate slide deck", "生成演示文稿", "スライド資料を生成", "Gerar apresentação de slides"),
    gen_human(
        "A slide deck from your sources, as PDF and PPTX.",
        "根据来源生成演示文稿，提供 PDF 和 PPTX。",
        "ソースからスライド資料を作成し、PDF と PPTX で返します。",
        "Uma apresentação de slides das suas fontes, em PDF e PPTX.",
    ),
    "Generate a NotebookLM slide deck; returns the PDF and PPTX files and each slide's text.",
    [
        select(
            "format",
            FMT_LABEL,
            L(
                "Detailed deck (default) or presenter slides.",
                "详细演示文稿（默认）或演讲者幻灯片。",
                "詳細なスライド（既定）またはプレゼンター用スライド。",
                "Apresentação detalhada (padrão) ou slides para apresentador.",
            ),
            SLIDES_FORMAT,
        ),
        select(
            "length",
            LEN_LABEL,
            L("Short, default or long.", "较短、默认或较长。", "短め・標準・長め。", "Curto, padrão ou longo."),
            LENGTH_3,
        ),
        LANGUAGE,
        INSTRUCTIONS,
        *generation_tail(True, 120, False),
    ],
    JOB_OUTPUT,
)

tool(
    "generate_infographic",
    L("Generate infographic", "生成信息图", "インフォグラフィックを生成", "Gerar infográfico"),
    gen_human(
        "A one-page infographic image (PNG) from your sources.",
        "根据来源生成单页信息图（PNG）。",
        "ソースから 1 枚のインフォグラフィック画像（PNG）を作成します。",
        "Um infográfico de uma página (PNG) das suas fontes.",
    ),
    "Generate a NotebookLM infographic; returns a PNG image and its text.",
    [
        select("style", STYLE_LABEL, L("Default: auto.", "默认：自动。", "既定は自動。", "Padrão: automático."), INFOGRAPHIC_STYLES),
        select(
            "orientation",
            L("Orientation", "方向", "向き", "Orientação"),
            L(
                "Landscape (default), portrait or square.",
                "横向（默认）、纵向或方形。",
                "横向き（既定）・縦向き・正方形。",
                "Paisagem (padrão), retrato ou quadrado.",
            ),
            ORIENTATION,
        ),
        select(
            "detail",
            L("Detail", "详细程度", "詳しさ", "Nível de detalhe"),
            L(
                "Concise, standard (default) or detailed.",
                "简洁、标准（默认）或详细。",
                "簡潔・標準（既定）・詳細。",
                "Conciso, padrão ou detalhado.",
            ),
            DETAIL,
        ),
        LANGUAGE,
        INSTRUCTIONS,
        *generation_tail(True, 120, False),
    ],
    JOB_OUTPUT,
)

tool(
    "generate_report",
    L("Generate report", "生成报告", "レポートを生成", "Gerar relatório"),
    gen_human(
        "A written report in Markdown: briefing, study guide, blog post or your own prompt.",
        "Markdown 格式的书面报告：简报、学习指南、博客文章或自定义提示。",
        "Markdown のレポート：ブリーフィング資料・学習ガイド・ブログ記事、または独自のプロンプト。",
        "Um relatório escrito em Markdown: briefing, guia de estudo, post de blog ou seu próprio prompt.",
    ),
    "Generate a NotebookLM report in Markdown. format: briefing (default), study_guide, blog_post, or custom (instructions become the whole prompt).",
    [
        select(
            "format",
            FMT_LABEL,
            L(
                "Briefing (default), study guide, blog post or custom.",
                "简报（默认）、学习指南、博客文章或自定义。",
                "ブリーフィング資料（既定）・学習ガイド・ブログ記事・カスタム。",
                "Briefing (padrão), guia de estudo, post de blog ou personalizado.",
            ),
            [
                opt("briefing", L("Briefing doc", "简报文档", "ブリーフィング資料", "Documento de briefing")),
                opt("study_guide", L("Study guide", "学习指南", "学習ガイド", "Guia de estudo")),
                opt("blog_post", L("Blog post", "博客文章", "ブログ記事", "Post de blog")),
                opt("custom", L("Custom (instructions)", "自定义（说明）", "カスタム（指示）", "Personalizado (instruções)")),
            ],
        ),
        LANGUAGE,
        INSTRUCTIONS,
        *generation_tail(False, 120, True),
    ],
    JOB_OUTPUT,
)

tool(
    "generate_interactive_report",
    L("Generate interactive report", "生成交互式报告", "インタラクティブレポートを生成", "Gerar relatório interativo"),
    gen_human(
        "An interactive report that also suggests infographics, slides, mind maps, quizzes and flashcards.",
        "交互式报告，还会推荐信息图、演示文稿、思维导图、测验和闪卡。",
        "インフォグラフィック・スライド・マインドマップ・テスト・フラッシュカードも提案するインタラクティブレポート。",
        "Um relatório interativo que também sugere infográficos, slides, mapas mentais, testes e cartões.",
    ),
    "Generate a NotebookLM interactive report; its suggested items can then be made with Generate a suggested item.",
    [LANGUAGE, INSTRUCTIONS, *generation_tail(False, 120, True)],
    JOB_OUTPUT,
)

tool(
    "generate_data_table",
    L("Generate data table", "生成数据表", "データ表を生成", "Gerar tabela de dados"),
    gen_human(
        "A table of facts extracted from your sources.",
        "从来源中提取事实生成的表格。",
        "ソースから事実を抽出した表。",
        "Uma tabela de fatos extraídos das suas fontes.",
    ),
    "Generate a NotebookLM data table from a notebook; returned as rows and as a Markdown table. Use instructions to say which columns you want.",
    [LANGUAGE, INSTRUCTIONS, *generation_tail(False, 120, True)],
    JOB_OUTPUT,
)

tool(
    "generate_quiz",
    L("Generate quiz", "生成测验", "テストを生成", "Gerar teste"),
    gen_human(
        "Multiple-choice questions with answers, rationales and hints.",
        "带答案、解析和提示的多项选择题。",
        "解答・解説・ヒント付きの多肢選択問題。",
        "Perguntas de múltipla escolha com respostas, justificativas e dicas.",
    ),
    "Generate a NotebookLM quiz; returns JSON and a readable list of questions with the correct options marked.",
    [*quantity_difficulty(), INSTRUCTIONS, *generation_tail(False, 120, True)],
    JOB_OUTPUT,
)

tool(
    "generate_flashcards",
    L("Generate flashcards", "生成闪卡", "フラッシュカードを生成", "Gerar cartões de estudo"),
    gen_human(
        "Study flashcards from your sources.",
        "根据来源生成学习闪卡。",
        "ソースから学習用フラッシュカードを作成します。",
        "Cartões de estudo das suas fontes.",
    ),
    "Generate NotebookLM flashcards; returns JSON and a readable list.",
    [*quantity_difficulty(), INSTRUCTIONS, *generation_tail(False, 120, True)],
    JOB_OUTPUT,
)

tool(
    "generate_mind_map",
    L("Generate mind map", "生成思维导图", "マインドマップを生成", "Gerar mapa mental"),
    gen_human(
        "A mind map of the topics in your sources.",
        "来源中各主题的思维导图。",
        "ソースのトピックをまとめたマインドマップ。",
        "Um mapa mental dos temas das suas fontes.",
    ),
    "Generate a NotebookLM mind map; returns the JSON tree and an indented outline.",
    [INSTRUCTIONS, *generation_tail(False, 120, True)],
    JOB_OUTPUT,
)

tool(
    "generate_suggested_item",
    L("Generate a suggested item", "生成推荐项", "提案アイテムを生成", "Gerar um item sugerido"),
    L(
        "Generate an infographic, slide deck, mind map, quiz or flashcards that an interactive report suggested.",
        "生成交互式报告推荐的信息图、演示文稿、思维导图、测验或闪卡。",
        "インタラクティブレポートが提案したインフォグラフィック・スライド・マインドマップ・テスト・フラッシュカードを生成します。",
        "Gera um infográfico, slides, mapa mental, teste ou cartões sugeridos por um relatório interativo.",
    ),
    "Generate an item suggested by a NotebookLM interactive report (its embedded artifact id). Options apply by type: orientation/detail/style for infographic, format/length for slides, quantity/difficulty for quiz and flashcards.",
    [
        ARTIFACT,
        INSTRUCTIONS,
        LANGUAGE,
        select(
            "orientation",
            L("Orientation (infographic)", "方向（信息图）", "向き（インフォグラフィック）", "Orientação (infográfico)"),
            L("Infographic only.", "仅限信息图。", "インフォグラフィックのみ。", "Só infográfico."),
            ORIENTATION,
        ),
        select(
            "detail",
            L("Detail (infographic)", "详细程度（信息图）", "詳しさ（インフォグラフィック）", "Detalhe (infográfico)"),
            L("Infographic only.", "仅限信息图。", "インフォグラフィックのみ。", "Só infográfico."),
            DETAIL,
        ),
        select(
            "style",
            L("Style (infographic)", "风格（信息图）", "スタイル（インフォグラフィック）", "Estilo (infográfico)"),
            L("Infographic only.", "仅限信息图。", "インフォグラフィックのみ。", "Só infográfico."),
            INFOGRAPHIC_STYLES,
        ),
        select(
            "format",
            L("Format (slides)", "格式（演示文稿）", "形式（スライド）", "Formato (slides)"),
            L("Slides only.", "仅限演示文稿。", "スライドのみ。", "Só slides."),
            SLIDES_FORMAT,
        ),
        select(
            "length",
            L("Length (slides)", "长度（演示文稿）", "長さ（スライド）", "Duração (slides)"),
            L("Slides only.", "仅限演示文稿。", "スライドのみ。", "Só slides."),
            LENGTH_3,
        ),
        select(
            "quantity",
            L("Number of items (quiz, flashcards)", "数量（测验、闪卡）", "数（テスト・フラッシュカード）", "Quantidade (teste, cartões)"),
            L("Quiz and flashcards only.", "仅限测验和闪卡。", "テストとフラッシュカードのみ。", "Só teste e cartões."),
            QUANTITY,
        ),
        select(
            "difficulty",
            L("Difficulty (quiz, flashcards)", "难度（测验、闪卡）", "難易度（テスト・フラッシュカード）", "Dificuldade (teste, cartões)"),
            L("Quiz and flashcards only.", "仅限测验和闪卡。", "テストとフラッシュカードのみ。", "Só teste e cartões."),
            DIFFICULTY,
        ),
        WAIT,
        MAX_WAIT(120),
        RETURN_FILE,
    ],
    JOB_OUTPUT,
)

tool(
    "retry_artifact",
    L("Retry failed artifact", "重试失败的成果", "失敗したアーティファクトを再試行", "Tentar de novo artefato com falha"),
    L(
        "Re-run a failed generation in place.",
        "原地重新运行失败的生成。",
        "失敗した生成をその場で再実行します。",
        "Executa de novo, no mesmo lugar, uma geração que falhou.",
    ),
    "Retry a NotebookLM artifact whose generation failed.",
    [ARTIFACT, WAIT, MAX_WAIT(120), RETURN_FILE],
    JOB_OUTPUT,
)

tool(
    "revise_slide",
    L("Revise a slide", "修改幻灯片", "スライドを修正", "Revisar um slide"),
    L(
        "Change one slide of a finished deck with a prompt.",
        "用提示修改已完成演示文稿中的一张幻灯片。",
        "完成したスライド資料の 1 枚を指示で修正します。",
        "Altera um slide de uma apresentação pronta com um prompt.",
    ),
    "Revise one slide of a completed NotebookLM slide deck.",
    [
        ARTIFACT,
        param(
            "slide",
            "number",
            L("Slide number", "幻灯片编号", "スライド番号", "Número do slide"),
            L("Counted from 1.", "从 1 开始计数。", "1 から数えます。", "Contado a partir de 1."),
            "The slide number, starting at 1.",
            required=True,
            min=1,
            max=500,
        ),
        param(
            "prompt",
            "string",
            L("What to change", "修改内容", "修正内容", "O que mudar"),
            L("1 to 2,000 characters.", "1 到 2,000 个字符。", "1〜2,000 文字。", "De 1 a 2.000 caracteres."),
            "What to change on the slide.",
            required=True,
        ),
        WAIT,
        MAX_WAIT(120),
        RETURN_FILE,
    ],
    JOB_OUTPUT,
)

# --- artifacts

tool(
    "list_artifacts",
    L("List artifacts", "列出成果", "アーティファクト一覧", "Listar artefatos"),
    L(
        "The Studio artifacts of a notebook (audio, video, slides, reports and more).",
        "笔记本的 Studio 成果（音频、视频、演示文稿、报告等）。",
        "ノートブックの Studio アーティファクト（音声、動画、スライド、レポートなど）。",
        "Os artefatos do Studio de um notebook (áudio, vídeo, slides, relatórios e mais).",
    ),
    "List the Studio artifacts of a NotebookLM notebook with type, status and id.",
    [NOTEBOOK()],
    {"artifact_ids": {"type": "array", "items": {"type": "string"}}},
)

tool(
    "get_artifact",
    L("Get artifact", "获取成果", "アーティファクトを取得", "Obter artefato"),
    L(
        "An artifact's content (text, table, quiz, mind map) and file links.",
        "成果的内容（文本、表格、测验、思维导图）和文件链接。",
        "アーティファクトの内容（テキスト・表・テスト・マインドマップ）とファイルのリンク。",
        "O conteúdo de um artefato (texto, tabela, teste, mapa mental) e os links dos arquivos.",
    ),
    "Get a NotebookLM artifact by id with its full result.",
    [
        ARTIFACT,
        param(
            "return_file",
            "boolean",
            L("Attach the file", "附加文件", "ファイルを添付", "Anexar o arquivo"),
            L(
                "Also download its audio, video, PDF/PPTX or image.",
                "同时下载其音频、视频、PDF/PPTX 或图片。",
                "音声・動画・PDF/PPTX・画像もダウンロードします。",
                "Também baixa o áudio, vídeo, PDF/PPTX ou imagem.",
            ),
            form="form",
            default=False,
        ),
    ],
    {"status": {"type": "string"}, "text": {"type": "string"}, "file_urls": {"type": "array", "items": {"type": "string"}}},
)

tool(
    "download_artifact",
    L("Download artifact file", "下载成果文件", "アーティファクトのファイルをダウンロード", "Baixar arquivo do artefato"),
    L(
        "Download one file of a finished artifact: m4a, mp4, pdf, pptx, png or a single slide image.",
        "下载已完成成果的单个文件：m4a、mp4、pdf、pptx、png 或单张幻灯片图片。",
        "完成したアーティファクトのファイルを 1 つダウンロード：m4a、mp4、pdf、pptx、png、スライド 1 枚の画像。",
        "Baixa um arquivo de um artefato pronto: m4a, mp4, pdf, pptx, png ou a imagem de um slide.",
    ),
    "Download a NotebookLM artifact file and return it as a Dify file.",
    [
        ARTIFACT,
        select(
            "format",
            L("File format", "文件格式", "ファイル形式", "Formato do arquivo"),
            L(
                "m4a (audio), mp4 (video), pdf/pptx (slides), png (infographic), slide (one slide image).",
                "m4a（音频）、mp4（视频）、pdf/pptx（演示文稿）、png（信息图）、slide（单张幻灯片图片）。",
                "m4a（音声）、mp4（動画）、pdf/pptx（スライド）、png（インフォグラフィック）、slide（スライド 1 枚の画像）。",
                "m4a (áudio), mp4 (vídeo), pdf/pptx (slides), png (infográfico), slide (imagem de um slide).",
            ),
            [
                opt("m4a", L("m4a (audio)", "m4a（音频）", "m4a（音声）", "m4a (áudio)")),
                opt("mp4", L("mp4 (video)", "mp4（视频）", "mp4（動画）", "mp4 (vídeo)")),
                opt("pdf", L("pdf (slides)", "pdf（演示文稿）", "pdf（スライド）", "pdf (slides)")),
                opt("pptx", L("pptx (slides)", "pptx（演示文稿）", "pptx（スライド）", "pptx (slides)")),
                opt("png", L("png (infographic)", "png（信息图）", "png（インフォグラフィック）", "png (infográfico)")),
                opt("slide", L("One slide image", "单张幻灯片图片", "スライド 1 枚の画像", "Imagem de um slide")),
            ],
            "File format: m4a, mp4, pdf, pptx, png or slide.",
        ),
        param(
            "index",
            "number",
            L("Slide number", "幻灯片编号", "スライド番号", "Número do slide"),
            L(
                "With format slide: the slide number, from 1.",
                "格式为 slide 时：幻灯片编号，从 1 开始。",
                "形式が slide のとき：スライド番号（1 から）。",
                "Com o formato slide: o número do slide, a partir de 1.",
            ),
            "Slide number (from 1), only with format slide.",
            min=1,
            max=500,
        ),
        param(
            "width",
            "number",
            L("Image width (px)", "图片宽度（像素）", "画像の幅（px）", "Largura da imagem (px)"),
            L(
                "Optional, png and slide only: scale down to this width (100 to 4096).",
                "可选，仅限 png 和 slide：缩小到此宽度（100 到 4096）。",
                "任意。png と slide のみ：この幅に縮小（100〜4096）。",
                "Opcional, só png e slide: reduz para esta largura (100 a 4096).",
            ),
            "Optional image width in pixels for png or slide, 100 to 4096.",
            min=100,
            max=4096,
        ),
    ],
)

tool(
    "delete_artifact",
    L("Delete artifact", "删除成果", "アーティファクトを削除", "Excluir artefato"),
    L(
        "Delete an artifact, or dismiss a suggested item.",
        "删除成果，或忽略推荐项。",
        "アーティファクトを削除、または提案アイテムを却下します。",
        "Exclui um artefato, ou descarta um item sugerido.",
    ),
    "Delete a NotebookLM artifact. Only when the user asks.",
    [ARTIFACT],
)

tool(
    "export_artifact",
    L(
        "Export to Google Docs or Sheets",
        "导出到 Google 文档或表格",
        "Google ドキュメント／スプレッドシートにエクスポート",
        "Exportar para Google Docs ou Planilhas",
    ),
    L(
        "Export a report to Google Docs or a data table to Google Sheets.",
        "将报告导出到 Google 文档，或将数据表导出到 Google 表格。",
        "レポートを Google ドキュメントに、データ表を Google スプレッドシートにエクスポートします。",
        "Exporta um relatório para o Google Docs ou uma tabela de dados para o Google Planilhas.",
    ),
    "Export a NotebookLM report to Google Docs (destination docs) or a data table to Google Sheets (destination sheets); returns the file URL.",
    [
        ARTIFACT,
        select(
            "destination",
            L("Destination", "导出目标", "エクスポート先", "Destino"),
            L(
                "Docs for a report, Sheets for a table.",
                "报告选文档，数据表选表格。",
                "レポートはドキュメント、表はスプレッドシート。",
                "Docs para relatório, Planilhas para tabela.",
            ),
            [
                opt("docs", L("Google Docs", "Google 文档", "Google ドキュメント", "Google Docs")),
                opt("sheets", L("Google Sheets", "Google 表格", "Google スプレッドシート", "Google Planilhas")),
            ],
            "docs for a report, sheets for a data table.",
        ),
        param(
            "title",
            "string",
            L("File name", "文件名", "ファイル名", "Nome do arquivo"),
            L(
                "Optional. Default: the artifact's title.",
                "可选。默认：成果标题。",
                "任意。既定はアーティファクトのタイトル。",
                "Opcional. Padrão: o título do artefato.",
            ),
            "Optional name of the new file.",
        ),
    ],
    {"url": {"type": "string"}},
)

# --- notes

NOTE = param(
    "note",
    "string",
    L("Note ID", "笔记 ID", "メモ ID", "ID da nota"),
    L(
        "A note id from List notes or Create note.",
        "来自“列出笔记”或“创建笔记”的笔记 ID。",
        "「メモ一覧」または「メモを作成」のメモ ID。",
        "Um ID de nota de Listar notas ou Criar nota.",
    ),
    "The note id.",
    required=True,
)

tool(
    "list_notes",
    L("List notes", "列出笔记", "メモ一覧", "Listar notas"),
    L("The notes saved in a notebook.", "笔记本中保存的笔记。", "ノートブックに保存されたメモ。", "As notas salvas em um notebook."),
    "List the notes of a NotebookLM notebook with their text.",
    [NOTEBOOK()],
)

tool(
    "create_note",
    L("Create note", "创建笔记", "メモを作成", "Criar nota"),
    L(
        "Save a note in a notebook, from text or from a whole chat conversation.",
        "在笔记本中保存笔记，内容可来自文本或整段聊天对话。",
        "テキスト、またはチャットの会話全体からメモをノートブックに保存します。",
        "Salva uma nota no notebook, a partir de texto ou de uma conversa inteira do chat.",
    ),
    "Create a note in a NotebookLM notebook from content, or from a chat conversation id (not both).",
    [
        NOTEBOOK(),
        param(
            "content",
            "string",
            L("Text", "文本", "テキスト", "Texto"),
            L(
                "The note's text (up to 500,000 characters).",
                "笔记文本（最多 500,000 个字符）。",
                "メモの本文（最大 500,000 文字）。",
                "O texto da nota (até 500.000 caracteres).",
            ),
            "The note text.",
        ),
        CONVERSATION,
        param(
            "title",
            "string",
            L("Title", "标题", "タイトル", "Título"),
            L("Optional, 1 to 200 characters.", "可选，1 到 200 个字符。", "任意。1〜200 文字。", "Opcional, de 1 a 200 caracteres."),
            "Optional note title.",
        ),
    ],
    {"note": {"type": "string"}},
)

tool(
    "delete_note",
    L("Delete note", "删除笔记", "メモを削除", "Excluir nota"),
    L("Delete a note.", "删除笔记。", "メモを削除します。", "Exclui uma nota."),
    "Delete a NotebookLM note.",
    [NOTE],
)

tool(
    "note_to_source",
    L("Convert note to source", "将笔记转为来源", "メモをソースに変換", "Converter nota em fonte"),
    L(
        "Turn a note into a source that chat and Studio can use.",
        "将笔记转为聊天和 Studio 可用的来源。",
        "メモをチャットと Studio で使えるソースに変換します。",
        "Transforma uma nota em fonte que o chat e o Studio podem usar.",
    ),
    "Convert a NotebookLM note into a source.",
    [NOTE],
)

# --- labels and collections

tool(
    "list_labels",
    L("List source labels", "列出来源标签", "ソースのラベル一覧", "Listar rótulos de fontes"),
    L(
        "The labels that group a notebook's sources.",
        "对笔记本来源进行分组的标签。",
        "ノートブックのソースをまとめるラベル。",
        "Os rótulos que agrupam as fontes de um notebook.",
    ),
    "List the source labels of a NotebookLM notebook.",
    [NOTEBOOK()],
)

tool(
    "create_labels",
    L("Label sources", "标记来源", "ソースにラベルを付ける", "Rotular fontes"),
    L(
        "Let Google group the sources by topic, or add one label of your own.",
        "让 Google 按主题对来源分组，或添加一个自定义标签。",
        "Google にトピック別でソースをまとめさせるか、独自のラベルを 1 つ追加します。",
        "Deixa o Google agrupar as fontes por tema, ou adiciona um rótulo seu.",
    ),
    "Auto-label a NotebookLM notebook's sources by topic (auto all or unlabeled), or create one named label.",
    [
        NOTEBOOK(),
        select(
            "auto",
            L("Auto-label", "自动标记", "自動ラベル", "Rotular automaticamente"),
            L(
                "All: relabel every source (replaces labels). Unlabeled: only sources without a label.",
                "全部：重新标记所有来源（替换现有标签）。未标记：仅标记无标签的来源。",
                "すべて：全ソースを付け直し（既存ラベルを置換）。未設定のみ：ラベルのないソースだけ。",
                "Todas: rotula de novo todas as fontes (substitui os rótulos). Sem rótulo: só as fontes sem rótulo.",
            ),
            [
                opt("all", L("All sources", "全部来源", "すべてのソース", "Todas as fontes")),
                opt("unlabeled", L("Unlabeled only", "仅未标记", "未設定のみ", "Só sem rótulo")),
            ],
        ),
        param(
            "name",
            "string",
            L("Label name", "标签名称", "ラベル名", "Nome do rótulo"),
            L(
                "Or: the name of a new label (1 to 100 characters).",
                "或者：新标签的名称（1 到 100 个字符）。",
                "または：新しいラベルの名前（1〜100 文字）。",
                "Ou: o nome de um novo rótulo (1 a 100 caracteres).",
            ),
            "Name of one new label; use instead of auto.",
        ),
        param(
            "emoji",
            "string",
            L("Emoji", "表情符号", "絵文字", "Emoji"),
            L(
                "Optional, with a label name.",
                "可选，配合标签名称使用。",
                "任意。ラベル名と一緒に指定。",
                "Opcional, com um nome de rótulo.",
            ),
            "Optional emoji for the named label.",
        ),
    ],
)

tool(
    "list_collections",
    L("List collections", "列出合集", "コレクション一覧", "Listar coleções"),
    L(
        "The collections that group notebooks.",
        "对笔记本进行分组的合集。",
        "ノートブックをまとめるコレクション。",
        "As coleções que agrupam notebooks.",
    ),
    "List the NotebookLM notebook collections.",
    [EMAIL("the Google account to list")],
)

tool(
    "create_collection",
    L("Create collection", "创建合集", "コレクションを作成", "Criar coleção"),
    L(
        "Create a collection to group notebooks.",
        "创建合集来对笔记本分组。",
        "ノートブックをまとめるコレクションを作成します。",
        "Cria uma coleção para agrupar notebooks.",
    ),
    "Create a NotebookLM collection. Pass email when the token has several accounts.",
    [
        param(
            "name",
            "string",
            L("Name", "名称", "名前", "Nome"),
            L("The collection's name.", "合集名称。", "コレクションの名前。", "O nome da coleção."),
            "Collection name.",
            required=True,
        ),
        param(
            "emoji", "string", L("Emoji", "表情符号", "絵文字", "Emoji"), L("Optional.", "可选。", "任意。", "Opcional."), "Optional emoji."
        ),
        EMAIL("the Google account to create the collection on"),
    ],
    {"collection": {"type": "string"}},
)

tool(
    "update_collection",
    L("Update collection", "更新合集", "コレクションを更新", "Atualizar coleção"),
    L(
        "Rename a collection, or add and remove notebooks.",
        "重命名合集，或添加、移除笔记本。",
        "コレクション名の変更、ノートブックの追加・削除を行います。",
        "Renomeia uma coleção, ou adiciona e remove notebooks.",
    ),
    "Rename a NotebookLM collection or add/remove notebooks.",
    [
        param(
            "collection",
            "string",
            L("Collection ID", "合集 ID", "コレクション ID", "ID da coleção"),
            L(
                "From List collections or Create collection.",
                "来自“列出合集”或“创建合集”。",
                "「コレクション一覧」または「コレクションを作成」から。",
                "De Listar coleções ou Criar coleção.",
            ),
            "The collection id.",
            required=True,
        ),
        param(
            "name",
            "string",
            L("New name", "新名称", "新しい名前", "Novo nome"),
            L("Optional.", "可选。", "任意。", "Opcional."),
            "Optional new name.",
        ),
        param(
            "add_notebooks",
            "string",
            L("Add notebooks", "添加笔记本", "ノートブックを追加", "Adicionar notebooks"),
            L("Notebook ids, one per line.", "笔记本 ID，每行一个。", "ノートブック ID を 1 行に 1 つ。", "IDs de notebook, um por linha."),
            "Notebook ids to add, separated by new lines.",
        ),
        param(
            "remove_notebooks",
            "string",
            L("Remove notebooks", "移除笔记本", "ノートブックを外す", "Remover notebooks"),
            L(
                "Notebook ids, one per line. The notebooks stay.",
                "笔记本 ID，每行一个。笔记本本身会保留。",
                "ノートブック ID を 1 行に 1 つ。ノートブック自体は残ります。",
                "IDs de notebook, um por linha. Os notebooks continuam existindo.",
            ),
            "Notebook ids to remove, separated by new lines.",
        ),
    ],
)
