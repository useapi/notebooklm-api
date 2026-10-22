"""One handler per Dify tool. Each handler yields Out items that runner.py turns
into Dify messages, so the handlers can be unit-tested without Dify.

API reference: https://useapi.net/docs/api-gemini-notebook-v1
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

from . import params as P
from .client import CHAT_TIMEOUT, UPLOAD_TIMEOUT, Client, FileTooLarge, UseapiError, enc
from .render import render_result, summarize_job

POLL_SECONDS = 15  # the API advances running jobs about every 15 seconds
DEFAULT_WAIT = 120  # agent friendly: Dify agents stop a turn at about 600 s
MAX_WAIT = 540  # stays under Dify's default 600 s plugin execution limit
MAX_FILE_BYTES = 150 * 1024 * 1024
RUNNING = ("pending", "processing")


@dataclass
class Out:
    kind: str  # text | json | var | blob | link
    value: Any
    name: str | None = None
    meta: dict[str, Any] | None = None


def text(value: str) -> Out:
    return Out("text", value)


def js(value: Any) -> Out:
    return Out("json", value if isinstance(value, (dict, list)) else {"result": value})


def var(name: str, value: Any) -> Out:
    return Out("var", value, name=name)


@dataclass
class Ctx:
    client: Client
    default_email: str | None = None
    sleep: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.monotonic
    log: list[str] = field(default_factory=list)

    def email(self, p: dict[str, Any]) -> str | None:
        return P.text(p, "email") or self.default_email

    def get(self, path: str, **kw: Any) -> Any:
        return self.client.request("GET", path, **kw)

    def post(self, path: str, body: dict[str, Any], **kw: Any) -> Any:
        return self.client.request("POST", path, body=body, **kw)

    def delete(self, path: str, **kw: Any) -> Any:
        return self.client.request("DELETE", path, **kw)


Handler = Callable[[Ctx, dict[str, Any]], Iterator[Out]]
HANDLERS: dict[str, Handler] = {}


def tool(name: str) -> Callable[[Handler], Handler]:
    def register(fn: Handler) -> Handler:
        HANDLERS[name] = fn
        return fn

    return register


def done(message: str, data: Any) -> Iterator[Out]:
    yield text(message)
    yield js(data)


# --------------------------------------------------------------------------- accounts


@tool("list_accounts")
def list_accounts(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("accounts")
    accounts = data if isinstance(data, dict) else {}
    lines = [f"{len(accounts)} Google account(s) connected."]
    for email, info in accounts.items():
        info = info if isinstance(info, dict) else {}
        lines.append(f"- {email}: health {info.get('health', '?')}, running {info.get('runningJobs', 0)}/{info.get('maxJobs', '?')} jobs")
    yield var("emails", list(accounts.keys()))
    yield from done("\n".join(lines), data)


@tool("get_account")
def get_account(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    email = ctx.email(p)
    if not email:
        raise UseapiError("Parameter 'email' is required (or set a default Google account email in the credentials).")
    data = ctx.get(f"accounts/{enc(email)}")
    yield from done(f"Account {email}: plan, live usage and limits are in the JSON output.", data)


@tool("list_jobs")
def list_jobs(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("jobs")
    accounts = (data or {}).get("accounts", {}) if isinstance(data, dict) else {}
    lines = []
    for email, info in accounts.items():
        jobs = info.get("jobs", []) if isinstance(info, dict) else []
        lines.append(f"- {email}: {len(jobs)} running job(s), health {info.get('health', '?')}")
        for job in jobs:
            lines.append(f"  - {job.get('type')} {job.get('jobid')} started {job.get('started_at')}")
    yield from done("\n".join(lines) or "No running jobs.", data)


# --------------------------------------------------------------------------- notebooks


@tool("list_notebooks")
def list_notebooks(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("notebooks/", params={"email": ctx.email(p)})
    lines: list[str] = []
    ids: list[str] = []
    for entry in data if isinstance(data, list) else []:
        if entry.get("error"):
            lines.append(f"{entry.get('email')}: error: {entry['error']}")
            continue
        notebooks = entry.get("notebooks", [])
        lines.append(f"{entry.get('email')}: {len(notebooks)} notebook(s)")
        for nb in notebooks:
            ids.append(nb.get("notebook"))
            lines.append(f"- {nb.get('title') or '(untitled)'} [{nb.get('sources', 0)} sources] id: {nb.get('notebook')}")
    yield var("notebook_ids", ids)
    yield from done("\n".join(lines) or "No notebooks found.", data)


@tool("create_notebook")
def create_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {}
    P.put(body, "email", ctx.email(p))
    P.put(body, "title", P.text(p, "title"))
    data = ctx.post("notebooks", body)
    yield var("notebook", data.get("notebook"))
    yield var("email", data.get("email"))
    yield from done(f"Created notebook '{data.get('title') or '(untitled)'}' on {data.get('email')}. id: {data.get('notebook')}", data)


@tool("get_notebook")
def get_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    nb = P.required(p, "notebook")
    data = ctx.get(f"notebooks/{enc(nb)}")
    sources = data.get("sources", []) if isinstance(data, dict) else []
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
    lines = [f"Notebook '{data.get('title') or '(untitled)'}': {len(sources)} source(s), {len(artifacts)} artifact(s)."]
    for s in sources:
        lines.append(f"- source [{s.get('status')}] {s.get('kind')}: {s.get('title')} id: {s.get('source')}")
    for a in artifacts:
        lines.append(f"- artifact [{a.get('status')}] {a.get('type')}: {a.get('title')} id: {a.get('artifact')}")
    yield var("source_ids", [s.get("source") for s in sources])
    yield var("ready", all(s.get("status") == "ready" for s in sources) if sources else False)
    yield from done("\n".join(lines), data)


@tool("rename_notebook")
def rename_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    nb = P.required(p, "notebook")
    data = ctx.post(f"notebooks/{enc(nb)}", {"title": P.required(p, "title")})
    yield from done("Notebook renamed.", data)


@tool("delete_notebook")
def delete_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    nb = P.required(p, "notebook")
    data = ctx.delete(f"notebooks/{enc(nb)}")
    yield from done("Notebook deleted, with its sources and artifacts.", data)


@tool("copy_notebook")
def copy_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body = {"notebook": P.required(p, "notebook")}
    P.put(body, "title", P.text(p, "title"))
    data = ctx.post("notebooks/copy", body)
    yield var("notebook", data.get("notebook") if isinstance(data, dict) else None)
    yield from done(f"Notebook copied. New id: {data.get('notebook') if isinstance(data, dict) else ''}", data)


@tool("get_notebook_guide")
def get_notebook_guide(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    nb = P.required(p, "notebook")
    data = ctx.get("notebooks/guide", params={"notebook": nb})
    parts = [data.get("summary") or "(no summary yet)"]
    questions = data.get("suggestedQuestions") or []
    if questions:
        parts.append("Suggested questions:")
        parts += [f"- {q.get('title') or q.get('prompt')}" for q in questions if isinstance(q, dict)]
    reports = data.get("suggestedReports") or []
    if reports:
        parts.append("Suggested reports:")
        parts += [f"- {r.get('title') or r.get('prompt')}" for r in reports if isinstance(r, dict)]
    yield var("summary", data.get("summary"))
    yield from done("\n".join(parts), data)


@tool("get_sharing")
def get_sharing(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("sharing", params={"notebook": P.required(p, "notebook")})
    yield from done("Sharing settings are in the JSON output.", data)


@tool("share_notebook")
def share_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook")}
    emails = P.items(p, "people_emails")
    if emails:
        role = P.text(p, "role") or "viewer"
        body["people"] = [{"email": e, "role": role} for e in emails]
    P.put(body, "link", P.text(p, "link"))
    allow = P.flag(p, "allow_copies")
    if allow is not None and body.get("link") != "restricted":
        body["allowCopies"] = allow
    P.put(body, "viewLevel", P.text(p, "view_level"))
    if not any(key in body for key in ("people", "link", "allowCopies", "viewLevel")):
        raise UseapiError("Nothing to change: give people_emails, link, allow_copies or view_level.")
    notify = P.flag(p, "notify")
    if notify is not None and "people" in body:
        body["notify"] = notify
    data = ctx.post("sharing", body)
    yield from done("Sharing updated.", data)


# --------------------------------------------------------------------------- sources


def _wait_sources(ctx: Ctx, notebook: str, source_ids: list[str], max_wait: int) -> dict[str, str]:
    """Poll the notebook until the given sources are ready or failed. Returns id -> status."""
    deadline = ctx.clock() + max_wait
    statuses: dict[str, str] = {}
    while True:
        data = ctx.get(f"notebooks/{enc(notebook)}")
        statuses = {s.get("source"): s.get("status") for s in data.get("sources", []) if s.get("source") in source_ids}
        pending = [sid for sid in source_ids if statuses.get(sid) not in ("ready", "error")]
        remaining = deadline - ctx.clock()
        if not pending or remaining <= 0:
            return statuses
        ctx.sleep(min(10, remaining))


def _sources_result(ctx: Ctx, p: dict[str, Any], notebook: str, sources: list[dict[str, Any]], data: Any) -> Iterator[Out]:
    ids = [s.get("source") for s in sources if s.get("source")]
    if P.flag(p, "wait_until_ready", True) and ids:
        statuses = _wait_sources(ctx, notebook, ids, P.number(p, "max_wait_seconds", DEFAULT_WAIT, 10, MAX_WAIT))
        for s in sources:
            s["status"] = statuses.get(s.get("source"), s.get("status"))
    lines = [f"{len(sources)} source(s) added to the notebook."]
    for s in sources:
        lines.append(f"- [{s.get('status')}] {s.get('kind')}: {s.get('title')} id: {s.get('source')}")
    not_ready = [s for s in sources if s.get("status") != "ready"]
    if not_ready:
        lines.append(
            "Some sources are not ready yet. Chat and Studio use only ready sources; check them with 'Get notebook' before generating."
        )
    yield var("source_ids", ids)
    yield var("ready", not not_ready)
    yield from done("\n".join(lines), data)


@tool("add_sources")
def add_sources(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    notebook = P.required(p, "notebook")
    body: dict[str, Any] = {"notebook": notebook}
    P.put(body, "urls", P.items(p, "urls"))
    P.put(body, "text", P.text(p, "text"))
    if body.get("text"):
        P.put(body, "title", P.text(p, "title"))
    P.put(body, "drive", P.json_list(p, "drive_files"))
    P.put(body, "books", P.items(p, "book_ids"))
    if len(body) == 1:
        raise UseapiError("Give at least one of: urls, text, drive_files or book_ids.")
    data = ctx.post("sources", body)
    yield from _sources_result(ctx, p, notebook, list(data.get("sources", [])), data)


@tool("upload_source")
def upload_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    notebook = P.required(p, "notebook")
    file = p.get("file")
    if file is None:
        raise UseapiError("Parameter 'file' is required.")
    blob = getattr(file, "blob", None)
    if blob is None:
        raise UseapiError("Could not read the uploaded file.")
    name = P.text(p, "name") or getattr(file, "filename", None)
    mime = getattr(file, "mime_type", None) or "application/octet-stream"
    data = ctx.client.request(
        "POST",
        "sources/upload",
        params={"notebook": notebook, "name": name},
        data=blob,
        content_type=mime,
        timeout=UPLOAD_TIMEOUT,
    )
    sources = data.get("sources") or ([data] if data.get("source") else [])
    yield from _sources_result(ctx, p, notebook, list(sources), data)


@tool("get_source")
def get_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    source = P.required(p, "source")
    data = ctx.get(f"sources/{enc(source)}", params={"content": "true" if P.flag(p, "include_content", False) else None})
    message = f"Source '{data.get('title')}': {data.get('kind')}, status {data.get('status')}."
    if data.get("content"):
        message += "\n\n" + str(data["content"])
    yield var("status", data.get("status"))
    yield var("content", data.get("content"))
    yield from done(message, data)


@tool("rename_source")
def rename_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    source = P.required(p, "source")
    data = ctx.post(f"sources/{enc(source)}", {"title": P.required(p, "title")})
    yield from done("Source renamed.", data)


@tool("delete_source")
def delete_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    source = P.required(p, "source")
    data = ctx.delete(f"sources/{enc(source)}")
    yield from done("Source deleted.", data)


@tool("sync_drive_source")
def sync_drive_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.post("sources/sync", {"source": P.required(p, "source")})
    yield from done("Google Drive source re-imported.", data)


@tool("append_to_source")
def append_to_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body = {"source": P.required(p, "source"), "text": P.required(p, "text")}
    P.put(body, "title", P.text(p, "title"))
    data = ctx.post("sources/append", body)
    yield from done("Text appended to the source.", data)


@tool("search_sources")
def search_sources(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook"), "query": P.required(p, "query")}
    P.put(body, "sources", P.items(p, "sources"))
    P.put(body, "limit", P.number(p, "limit", None, 1, 100))
    data = ctx.post("sources/search", body)
    results = data.get("results", []) if isinstance(data, dict) else []
    lines = [f"{len(results)} matching passage(s)."]
    for i, item in enumerate(results, 1):
        if isinstance(item, dict):
            lines.append(f"[{i}] {str(item.get('text', ''))[:500]}\n    source: {item.get('source', '')}")
    yield var("passages", [r.get("text") for r in results if isinstance(r, dict)])
    yield from done("\n".join(lines), data)


@tool("list_play_books")
def list_play_books(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("sources/books", params={"email": ctx.email(p)})
    yield from done("Google Play Books library (use 'book' ids with 'Add sources').", data)


# --------------------------------------------------------------------------- chat


@tool("ask_notebook")
def ask_notebook(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook"), "question": P.required(p, "question")}
    P.put(body, "conversation", P.text(p, "conversation"))
    P.put(body, "sources", P.items(p, "sources"))
    data = ctx.post("chat", body, timeout=CHAT_TIMEOUT)
    answer = data.get("answer") or ""
    if not answer.strip():
        raise UseapiError("Gemini Notebook (NotebookLM) returned an empty answer. Wait a minute and ask again.")
    citations = data.get("citations") or []
    message = answer
    if citations:
        refs = [f"[{c.get('number')}] {' '.join(str(c.get('text') or '').split())[:300]}" for c in citations]
        message += "\n\nCitations:\n" + "\n".join(refs)
    yield var("answer", answer)
    yield var("conversation", data.get("conversation"))
    yield var("citations", citations)
    yield from done(message, data)


@tool("get_chat_history")
def get_chat_history(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("chat", params={"notebook": P.required(p, "notebook"), "conversation": P.text(p, "conversation")})
    yield from done("Chat history is in the JSON output.", data)


@tool("clear_chat")
def clear_chat(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.delete("chat", params={"notebook": P.required(p, "notebook"), "conversation": P.text(p, "conversation")})
    yield from done("Chat conversation cleared.", data)


@tool("configure_chat")
def configure_chat(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook")}
    P.put(body, "goal", P.text(p, "goal"))
    P.put(body, "persona", P.text(p, "persona"))
    P.put(body, "length", P.text(p, "length"))
    if len(body) == 1:
        raise UseapiError("Give goal, persona or length.")
    data = ctx.post("chat/settings", body)
    yield from done("Chat settings updated.", data)


# --------------------------------------------------------------------------- jobs (shared)


def _poll(ctx: Ctx, job: dict[str, Any], max_wait: int) -> dict[str, Any]:
    deadline = ctx.clock() + max_wait
    while job.get("status") in RUNNING and job.get("jobid"):
        remaining = deadline - ctx.clock()
        if remaining <= 0:
            break
        ctx.sleep(min(POLL_SECONDS, remaining))
        job = ctx.get(f"jobs/{enc(job['jobid'])}")
    return job


def _start_job(ctx: Ctx, path: str, body: dict[str, Any]) -> dict[str, Any]:
    """Start a job in async mode. Falls back to sync mode when async is unavailable."""
    try:
        return ctx.post(path, {**body, "mode": "async"}, ok_job_record=True)
    except UseapiError as e:
        if e.status == 503 and "Async mode is unavailable" in str(e.body):
            return ctx.post(path, {**body, "mode": "sync"}, ok_job_record=True, timeout=120)
        raise


def _files_out(ctx: Ctx, result: dict[str, Any], title: str) -> Iterator[Out]:
    for f in result.get("files") or []:
        url = f.get("url")
        if not url:
            continue
        try:
            blob, mime, filename = ctx.client.download(url, max_bytes=MAX_FILE_BYTES)
        except FileTooLarge as e:
            yield text(
                f"The {f.get('format')} file is {e.size // (1024 * 1024)} MB, too large to attach. "
                "Use 'Download artifact file' on a smaller format, or fetch the link with your API token."
            )
            continue
        name = filename or f"{(title or 'notebooklm').strip()[:80]}.{f.get('format', 'bin')}"
        yield Out("blob", blob, meta={"mime_type": f.get("mimeType") or mime, "filename": name})


JOB_NAMES = {
    "audio": "Audio Overview",
    "video": "Video Overview",
    "slides": "Slide deck",
    "infographic": "Infographic",
    "report": "Report",
    "interactive_report": "Interactive report",
    "table": "Data table",
    "quiz": "Quiz",
    "flashcards": "Flashcards",
    "mindmap": "Mind map",
    "research": "Research",
}


def finish_job(ctx: Ctx, job: dict[str, Any], p: dict[str, Any]) -> Iterator[Out]:
    if P.flag(p, "wait", True):
        job = _poll(ctx, job, P.number(p, "max_wait_seconds", DEFAULT_WAIT, 10, MAX_WAIT))
    status = job.get("status")
    result = job.get("result") if isinstance(job.get("result"), dict) else {}
    kind = JOB_NAMES.get(job.get("type"), str(job.get("type") or "The"))
    if status == "failed":
        err = job.get("error") or {}
        retry = f" Usage resets at {err['retryAt']}." if err.get("retryAt") else ""
        raise UseapiError(
            f"{kind} job failed ({err.get('code', 'error')}): {err.get('message', '')}{retry} jobid: {job.get('jobid')}",
            body=job,
        )
    if status in RUNNING:
        yield text(
            f"{kind} is still generating (job {job.get('jobid')}, status {status}). "
            "Call 'Get job status' (get_job) with this jobid and wait=true to get the result"
            + (" and the file." if job.get("type") in ("audio", "video", "slides", "infographic") else ".")
            + " Do not start the generation again."
        )
        yield js(job)
        yield var("jobid", job.get("jobid"))
        yield var("status", status)
        yield var("notebook", job.get("notebook"))
        yield var("artifact", job.get("artifact"))
        return
    rendered = render_result(job.get("type"), result)
    yield text(summarize_job(job) + ("\n\n" + rendered if rendered else ""))
    yield js(job)
    yield var("jobid", job.get("jobid"))
    yield var("status", status)
    yield var("notebook", job.get("notebook"))
    yield var("artifact", job.get("artifact"))
    yield var("title", result.get("title"))
    yield var("text", rendered)
    yield var("file_urls", [f.get("url") for f in result.get("files") or [] if f.get("url")])
    if P.flag(p, "return_file", True):
        yield from _files_out(ctx, result, result.get("title") or job.get("type"))


@tool("get_job")
def get_job(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    job = ctx.get(f"jobs/{enc(P.required(p, 'jobid'))}")
    yield from finish_job(ctx, job, p)


@tool("cancel_job")
def cancel_job(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.delete(f"jobs/{enc(P.required(p, 'jobid'))}")
    yield from done("Job cancelled and its slot freed. Google may still finish the artifact in the notebook.", data)


# --------------------------------------------------------------------------- research


@tool("research")
def research(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook"), "query": P.required(p, "query")}
    P.put(body, "type", P.text(p, "type"))
    P.put(body, "source", P.text(p, "source"))
    P.put(body, "replyUrl", P.text(p, "reply_url"))
    job = _start_job(ctx, "research", body)
    yield from finish_job(ctx, job, p)


@tool("import_research")
def import_research(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"jobid": P.required(p, "jobid")}
    P.put(body, "urls", P.items(p, "urls"))
    report = P.flag(p, "include_report")
    if report is not None:
        body["report"] = report
    data = ctx.post("research/import", body)
    sources = data.get("sources", []) if isinstance(data, dict) else []
    yield var("source_ids", [s.get("source") for s in sources if isinstance(s, dict)])
    yield from done(f"Imported {len(sources)} source(s) into the research job's notebook.", data)


# --------------------------------------------------------------------------- Studio generation

TEXT_TYPES = ("report", "interactive_report", "table", "quiz", "flashcards", "mindmap")

# tool parameter -> API field, per artifact type (see POST /artifacts "Options by type")
TYPE_OPTIONS: dict[str, dict[str, str]] = {
    "audio": {"format": "format", "length": "length", "language": "language", "instructions": "instructions"},
    "video": {"format": "format", "style": "style", "style_prompt": "stylePrompt", "language": "language", "instructions": "instructions"},
    "slides": {"format": "format", "length": "length", "language": "language", "instructions": "instructions"},
    "infographic": {
        "style": "style",
        "orientation": "orientation",
        "detail": "detail",
        "language": "language",
        "instructions": "instructions",
    },
    "report": {"format": "format", "language": "language", "instructions": "instructions"},
    "interactive_report": {"language": "language", "instructions": "instructions"},
    "table": {"language": "language", "instructions": "instructions"},
    "quiz": {"quantity": "quantity", "difficulty": "difficulty", "instructions": "instructions"},
    "flashcards": {"quantity": "quantity", "difficulty": "difficulty", "instructions": "instructions"},
    "mindmap": {"instructions": "instructions"},
}


def build_artifact_body(ctx: Ctx, kind: str, p: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    body: dict[str, Any] = {"type": kind}
    notes: list[str] = []
    for param, field_name in TYPE_OPTIONS[kind].items():
        P.put(body, field_name, P.text(p, param))
    if kind == "video":
        fmt = body.get("format")
        if fmt in ("cinematic", "short"):
            for key in ("style", "stylePrompt"):
                if body.pop(key, None):
                    notes.append(f"'{key}' was ignored: the {fmt} format has a fixed style.")
        if fmt == "cinematic":
            for key in ("language", "instructions"):
                if body.pop(key, None):
                    notes.append(f"'{key}' was ignored: the cinematic format does not take it.")
        if body.get("style") == "custom" and not body.get("stylePrompt"):
            raise UseapiError("Style 'custom' needs a style prompt.")
        if body.get("stylePrompt") and body.get("style") != "custom":
            body["style"] = "custom"
    if kind == "report" and body.get("format") == "custom" and not body.get("instructions"):
        raise UseapiError("Report format 'custom' needs instructions (the whole prompt).")

    notebook = P.text(p, "notebook")
    if notebook:
        body["notebook"] = notebook
        P.put(body, "sources", P.items(p, "sources"))
    else:
        urls = P.items(p, "urls")
        source_text = P.text(p, "text")
        if not urls and not source_text:
            raise UseapiError("Give a notebook id, or urls and/or text to create a one-shot notebook.")
        P.put(body, "urls", urls)
        P.put(body, "text", source_text)
        P.put(body, "title", P.text(p, "title"))
        P.put(body, "email", ctx.email(p))
        if P.flag(p, "delete_notebook", False):
            if kind in TEXT_TYPES:
                body["deleteNotebook"] = True
            else:
                notes.append("delete_notebook was ignored: media files are served from their notebook.")
    P.put(body, "replyUrl", P.text(p, "reply_url"))
    return body, notes


def _generator(kind: str) -> Handler:
    def handler(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
        body, notes = build_artifact_body(ctx, kind, p)
        for note in notes:
            yield text(note)
        job = _start_job(ctx, "artifacts", body)
        yield from finish_job(ctx, job, p)

    return handler


for _name, _kind in (
    ("generate_audio_overview", "audio"),
    ("generate_video_overview", "video"),
    ("generate_slide_deck", "slides"),
    ("generate_infographic", "infographic"),
    ("generate_report", "report"),
    ("generate_interactive_report", "interactive_report"),
    ("generate_data_table", "table"),
    ("generate_quiz", "quiz"),
    ("generate_flashcards", "flashcards"),
    ("generate_mind_map", "mindmap"),
):
    HANDLERS[_name] = _generator(_kind)


@tool("generate_suggested_item")
def generate_suggested_item(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"artifact": P.required(p, "artifact")}
    for name in ("instructions", "language", "orientation", "detail", "style", "format", "length", "quantity", "difficulty"):
        P.put(body, name, P.text(p, name))
    job = _start_job(ctx, "artifacts/generate", body)
    yield from finish_job(ctx, job, p)


@tool("retry_artifact")
def retry_artifact(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    job = _start_job(ctx, "artifacts/retry", {"artifact": P.required(p, "artifact")})
    yield from finish_job(ctx, job, p)


@tool("revise_slide")
def revise_slide(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body = {
        "artifact": P.required(p, "artifact"),
        "slide": P.number(p, "slide", 1, 1, 500),
        "prompt": P.required(p, "prompt"),
    }
    job = _start_job(ctx, "artifacts/revise", body)
    yield from finish_job(ctx, job, p)


# --------------------------------------------------------------------------- artifacts


@tool("list_artifacts")
def list_artifacts(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("artifacts", params={"notebook": P.required(p, "notebook")})
    items = data if isinstance(data, list) else []
    lines = [f"{len(items)} artifact(s)."]
    lines += [f"- [{a.get('status')}] {a.get('type')}: {a.get('title')} id: {a.get('artifact')}" for a in items]
    yield var("artifact_ids", [a.get("artifact") for a in items])
    yield from done("\n".join(lines), data)


@tool("get_artifact")
def get_artifact(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get(f"artifacts/{enc(P.required(p, 'artifact'))}")
    rendered = render_result(data.get("type"), data) if data.get("status") == "completed" else ""
    yield var("status", data.get("status"))
    yield var("text", rendered)
    yield var("file_urls", [f.get("url") for f in data.get("files") or [] if f.get("url")])
    yield text(f"{data.get('type')} '{data.get('title')}' is {data.get('status')}." + ("\n\n" + rendered if rendered else ""))
    yield js(data)
    if data.get("status") == "completed" and P.flag(p, "return_file", False):
        yield from _files_out(ctx, data, data.get("title") or data.get("type"))


@tool("download_artifact")
def download_artifact(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    artifact = P.required(p, "artifact")
    fmt = P.required(p, "format")
    query: dict[str, Any] = {"artifact": artifact, "format": fmt}
    if fmt == "slide":
        query["index"] = P.number(p, "index", 1, 1, 500)
    if fmt in ("png", "slide"):
        query["width"] = P.number(p, "width", None, 100, 4096)
    url = ctx.client.url("artifacts/download") + "?" + "&".join(f"{k}={enc(v)}" for k, v in query.items() if v is not None)
    try:
        blob, mime, filename = ctx.client.download(url, max_bytes=MAX_FILE_BYTES)
    except FileTooLarge as e:
        raise UseapiError(f"The file is {e.size // (1024 * 1024)} MB, too large to attach in Dify.") from e
    name = filename or f"notebooklm.{'png' if fmt == 'slide' else fmt}"
    yield text(f"Downloaded {name} ({len(blob) // 1024} KB).")
    yield Out("blob", blob, meta={"mime_type": mime, "filename": name})


@tool("delete_artifact")
def delete_artifact(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.delete(f"artifacts/{enc(P.required(p, 'artifact'))}")
    yield from done("Artifact deleted.", data)


@tool("export_artifact")
def export_artifact(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body = {"artifact": P.required(p, "artifact"), "destination": P.required(p, "destination")}
    P.put(body, "title", P.text(p, "title"))
    data = ctx.post("artifacts/export", body)
    link = data.get("url") if isinstance(data, dict) else None
    yield var("url", link)
    yield from done(f"Exported.{' ' + link if link else ''}", data)


# --------------------------------------------------------------------------- notes


@tool("list_notes")
def list_notes(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("notes", params={"notebook": P.required(p, "notebook")})
    notes = data if isinstance(data, list) else (data.get("notes", []) if isinstance(data, dict) else [])
    lines = [f"{len(notes)} note(s)."] + [f"- {n.get('title')} id: {n.get('note')}" for n in notes if isinstance(n, dict)]
    yield from done("\n".join(lines), data)


@tool("create_note")
def create_note(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook")}
    content = P.text(p, "content")
    conversation = P.text(p, "conversation")
    if bool(content) == bool(conversation):
        raise UseapiError("Give either content or conversation, not both.")
    P.put(body, "content", content)
    P.put(body, "conversation", conversation)
    P.put(body, "title", P.text(p, "title"))
    data = ctx.post("notes", body)
    yield var("note", data.get("note") if isinstance(data, dict) else None)
    yield from done("Note created.", data)


@tool("delete_note")
def delete_note(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.delete(f"notes/{enc(P.required(p, 'note'))}")
    yield from done("Note deleted.", data)


@tool("note_to_source")
def note_to_source(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.post("notes/source", {"note": P.required(p, "note")})
    yield from done("Note converted to a source.", data)


# --------------------------------------------------------------------------- labels and collections


@tool("list_labels")
def list_labels(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("labels", params={"notebook": P.required(p, "notebook")})
    yield from done("Source labels are in the JSON output.", data)


@tool("create_labels")
def create_labels(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"notebook": P.required(p, "notebook")}
    auto = P.text(p, "auto")
    name = P.text(p, "name")
    if bool(auto) == bool(name):
        raise UseapiError("Give either auto (let Google label by topic) or name (one label of your own).")
    P.put(body, "auto", auto)
    P.put(body, "name", name)
    if name:
        P.put(body, "emoji", P.text(p, "emoji"))
    data = ctx.post("labels", body)
    yield from done("Labels created.", data)


@tool("list_collections")
def list_collections(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    data = ctx.get("collections", params={"email": ctx.email(p)})
    yield from done("Collections are in the JSON output.", data)


@tool("create_collection")
def create_collection(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    body: dict[str, Any] = {"name": P.required(p, "name")}
    P.put(body, "emoji", P.text(p, "emoji"))
    P.put(body, "email", ctx.email(p))
    data = ctx.post("collections", body)
    yield var("collection", data.get("collection") if isinstance(data, dict) else None)
    yield from done("Collection created.", data)


@tool("update_collection")
def update_collection(ctx: Ctx, p: dict[str, Any]) -> Iterator[Out]:
    collection = P.required(p, "collection")
    body: dict[str, Any] = {}
    P.put(body, "name", P.text(p, "name"))
    P.put(body, "addNotebooks", P.items(p, "add_notebooks"))
    P.put(body, "removeNotebooks", P.items(p, "remove_notebooks"))
    if not body:
        raise UseapiError("Give name, add_notebooks or remove_notebooks.")
    data = ctx.post(f"collections/{enc(collection)}", body)
    yield from done("Collection updated.", data)
