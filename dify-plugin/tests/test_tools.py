"""Every tool against a mocked HTTP layer: method, path, query and body."""

from __future__ import annotations

import pytest

from fakes import FakeResponse, make_ctx, outs, run, vars_of
from useapi_notebook.client import BASE_URL, UseapiError
from useapi_notebook.handlers import HANDLERS

NB = "user:12345-user@example.com-notebook:d02c903b-17f8-4241-a263-2be9e7359d55"
SRC = "user:12345-user@example.com-source:d02c903b-17f8-4241-a263-2be9e7359d55:c1182943-b7f0-4e89-82bc-8b3614cfb78f"
ART = "user:12345-user@example.com-artifact:d02c903b-17f8-4241-a263-2be9e7359d55:0c2ba8dc-47dd-474f-a19c-c06896e269fd"
JOB = "job:12597f9a-010c-4758-8e9a-b5cc17b0ccdb-user:12345-user@example.com-bot:gemini_notebook"
NOTE = "user:12345-user@example.com-note:d02c903b-17f8-4241-a263-2be9e7359d55:e5514ee8-22e5-414d-aa67-86e8476ece09"
COL = "user:12345-user@example.com-collection:7f3b9e21-4c8a-4d6f-b2e5-1a9c0d8e6f43"
DL = f"{BASE_URL}/artifacts/download?artifact=x&format=m4a"


def job(status="completed", kind="audio", result=None, **extra):
    record = {"jobid": JOB, "email": "user@example.com", "type": kind, "status": status, "notebook": NB, "artifact": ART}
    if status == "completed":
        record["result"] = (
            result
            if result is not None
            else {"title": "Podcast", "duration": 277, "files": [{"format": "m4a", "mimeType": "audio/mp4", "url": DL}]}
        )
    record.update(extra)
    return record


NOWAIT = {"wait": False, "return_file": False}

# name, params, method, path, expected query subset, expected body subset
CASES = [
    ("list_accounts", {}, "GET", "accounts", {}, None),
    ("get_account", {"email": "a@b.com"}, "GET", "accounts/a@b.com", {}, None),
    ("list_jobs", {}, "GET", "jobs", {}, None),
    ("get_job", {"jobid": JOB, **NOWAIT}, "GET", f"jobs/{JOB}", {}, None),
    ("cancel_job", {"jobid": JOB}, "DELETE", f"jobs/{JOB}", {}, None),
    ("list_notebooks", {"email": "a@b.com"}, "GET", "notebooks/", {"email": "a@b.com"}, None),
    ("create_notebook", {"title": "Apollo 11"}, "POST", "notebooks", {}, {"title": "Apollo 11"}),
    ("get_notebook", {"notebook": NB}, "GET", f"notebooks/{NB}", {}, None),
    ("rename_notebook", {"notebook": NB, "title": "New"}, "POST", f"notebooks/{NB}", {}, {"title": "New"}),
    ("delete_notebook", {"notebook": NB}, "DELETE", f"notebooks/{NB}", {}, None),
    ("copy_notebook", {"notebook": NB, "title": "Copy"}, "POST", "notebooks/copy", {}, {"notebook": NB, "title": "Copy"}),
    ("get_notebook_guide", {"notebook": NB}, "GET", "notebooks/guide", {"notebook": NB}, None),
    ("get_sharing", {"notebook": NB}, "GET", "sharing", {"notebook": NB}, None),
    (
        "share_notebook",
        {"notebook": NB, "people_emails": "x@y.com\nz@y.com", "role": "editor", "link": "public", "allow_copies": False, "notify": False},
        "POST",
        "sharing",
        {},
        {
            "notebook": NB,
            "people": [{"email": "x@y.com", "role": "editor"}, {"email": "z@y.com", "role": "editor"}],
            "link": "public",
            "allowCopies": False,
            "notify": False,
        },
    ),
    (
        "add_sources",
        {"notebook": NB, "urls": "https://a.com\nhttps://youtu.be/x", "text": "hello", "title": "T", "wait_until_ready": False},
        "POST",
        "sources",
        {},
        {"notebook": NB, "urls": ["https://a.com", "https://youtu.be/x"], "text": "hello", "title": "T"},
    ),
    ("get_source", {"source": SRC, "include_content": True}, "GET", f"sources/{SRC}", {"content": "true"}, None),
    ("rename_source", {"source": SRC, "title": "T"}, "POST", f"sources/{SRC}", {}, {"title": "T"}),
    ("delete_source", {"source": SRC}, "DELETE", f"sources/{SRC}", {}, None),
    ("sync_drive_source", {"source": SRC}, "POST", "sources/sync", {}, {"source": SRC}),
    (
        "append_to_source",
        {"source": SRC, "text": "more", "title": "H"},
        "POST",
        "sources/append",
        {},
        {"source": SRC, "text": "more", "title": "H"},
    ),
    (
        "search_sources",
        {"notebook": NB, "query": "oxygen", "limit": 5},
        "POST",
        "sources/search",
        {},
        {"notebook": NB, "query": "oxygen", "limit": 5},
    ),
    ("list_play_books", {"email": "a@b.com"}, "GET", "sources/books", {"email": "a@b.com"}, None),
    (
        "ask_notebook",
        {"notebook": NB, "question": "Why?", "conversation": "c1", "sources": f"{SRC}"},
        "POST",
        "chat",
        {},
        {"notebook": NB, "question": "Why?", "conversation": "c1", "sources": [SRC]},
    ),
    ("get_chat_history", {"notebook": NB, "conversation": "c1"}, "GET", "chat", {"notebook": NB, "conversation": "c1"}, None),
    ("clear_chat", {"notebook": NB}, "DELETE", "chat", {"notebook": NB}, None),
    (
        "configure_chat",
        {"notebook": NB, "goal": "learning_guide", "length": "shorter"},
        "POST",
        "chat/settings",
        {},
        {"notebook": NB, "goal": "learning_guide", "length": "shorter"},
    ),
    (
        "research",
        {"notebook": NB, "query": "Q", "type": "deep", **NOWAIT},
        "POST",
        "research",
        {},
        {"notebook": NB, "query": "Q", "type": "deep", "mode": "async"},
    ),
    (
        "import_research",
        {"jobid": JOB, "urls": "https://a.com", "include_report": False},
        "POST",
        "research/import",
        {},
        {"jobid": JOB, "urls": ["https://a.com"], "report": False},
    ),
    (
        "generate_audio_overview",
        {"notebook": NB, "format": "debate", "length": "short", "language": "es", "instructions": "Risks", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {
            "type": "audio",
            "notebook": NB,
            "format": "debate",
            "length": "short",
            "language": "es",
            "instructions": "Risks",
            "mode": "async",
        },
    ),
    (
        "generate_video_overview",
        {"notebook": NB, "format": "brief", "style": "watercolor", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "video", "format": "brief", "style": "watercolor"},
    ),
    (
        "generate_slide_deck",
        {"notebook": NB, "format": "presenter", "length": "long", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "slides", "format": "presenter", "length": "long"},
    ),
    (
        "generate_infographic",
        {"notebook": NB, "style": "sketch_note", "orientation": "portrait", "detail": "concise", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "infographic", "style": "sketch_note", "orientation": "portrait", "detail": "concise"},
    ),
    (
        "generate_report",
        {"notebook": NB, "format": "study_guide", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "report", "format": "study_guide"},
    ),
    (
        "generate_interactive_report",
        {"notebook": NB, "language": "ja", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "interactive_report", "language": "ja"},
    ),
    (
        "generate_data_table",
        {"notebook": NB, "instructions": "Columns: date, event", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "table", "instructions": "Columns: date, event"},
    ),
    (
        "generate_quiz",
        {"urls": "https://a.com", "quantity": "more", "difficulty": "hard", "delete_notebook": True, **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "quiz", "urls": ["https://a.com"], "quantity": "more", "difficulty": "hard", "deleteNotebook": True},
    ),
    (
        "generate_flashcards",
        {"notebook": NB, "quantity": "fewer", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "flashcards", "quantity": "fewer"},
    ),
    (
        "generate_mind_map",
        {"notebook": NB, "instructions": "Focus", **NOWAIT},
        "POST",
        "artifacts",
        {},
        {"type": "mindmap", "instructions": "Focus"},
    ),
    (
        "generate_suggested_item",
        {"artifact": ART, "orientation": "square", **NOWAIT},
        "POST",
        "artifacts/generate",
        {},
        {"artifact": ART, "orientation": "square", "mode": "async"},
    ),
    ("retry_artifact", {"artifact": ART, **NOWAIT}, "POST", "artifacts/retry", {}, {"artifact": ART, "mode": "async"}),
    (
        "revise_slide",
        {"artifact": ART, "slide": 3, "prompt": "Bigger title", **NOWAIT},
        "POST",
        "artifacts/revise",
        {},
        {"artifact": ART, "slide": 3, "prompt": "Bigger title"},
    ),
    ("list_artifacts", {"notebook": NB}, "GET", "artifacts", {"notebook": NB}, None),
    ("get_artifact", {"artifact": ART}, "GET", f"artifacts/{ART}", {}, None),
    ("delete_artifact", {"artifact": ART}, "DELETE", f"artifacts/{ART}", {}, None),
    (
        "export_artifact",
        {"artifact": ART, "destination": "docs", "title": "Brief"},
        "POST",
        "artifacts/export",
        {},
        {"artifact": ART, "destination": "docs", "title": "Brief"},
    ),
    ("list_notes", {"notebook": NB}, "GET", "notes", {"notebook": NB}, None),
    (
        "create_note",
        {"notebook": NB, "content": "Text", "title": "T"},
        "POST",
        "notes",
        {},
        {"notebook": NB, "content": "Text", "title": "T"},
    ),
    ("delete_note", {"note": NOTE}, "DELETE", f"notes/{NOTE}", {}, None),
    ("note_to_source", {"note": NOTE}, "POST", "notes/source", {}, {"note": NOTE}),
    ("list_labels", {"notebook": NB}, "GET", "labels", {"notebook": NB}, None),
    ("create_labels", {"notebook": NB, "auto": "unlabeled"}, "POST", "labels", {}, {"notebook": NB, "auto": "unlabeled"}),
    ("list_collections", {}, "GET", "collections", {}, None),
    ("create_collection", {"name": "Space", "email": "a@b.com"}, "POST", "collections", {}, {"name": "Space", "email": "a@b.com"}),
    ("update_collection", {"collection": COL, "add_notebooks": NB}, "POST", f"collections/{COL}", {}, {"addNotebooks": [NB]}),
]

CANNED = {
    "jobs/": job(),
    "artifacts": job(),
    "research": job(kind="research", result={"mode": "deep", "query": "Q", "report": {"title": "R", "markdown": "# R"}, "sources": []}),
    "sources": {"notebook": NB, "sources": [{"source": SRC, "title": "A", "kind": "web", "status": "ready"}]},
    "notebooks/guide": {"summary": "S", "suggestedQuestions": [{"title": "Q1"}], "suggestedReports": []},
}


def routes_for(name):
    routes = [
        ("GET", "jobs/", job()),
        ("GET", "notebooks/guide", CANNED["notebooks/guide"]),
        ("POST", "research/import", {"notebook": NB, "sources": []}),
        ("POST", "research", CANNED["research"]),
        ("POST", "artifacts/export", {"url": "https://docs.google.com/document/d/x"}),
        ("POST", "artifacts", job()),
        ("GET", f"artifacts/{ART}", {"artifact": ART, "type": "report", "status": "completed", "title": "R", "text": "# R"}),
        ("POST", "sources/", {}),
        ("POST", "sources", CANNED["sources"]),
        ("POST", "chat", {"answer": "Because [1].", "conversation": "c1", "citations": [{"number": 1, "source": SRC, "text": "quote"}]}),
    ]
    return routes


def test_every_tool_has_a_case():
    # upload_source and download_artifact carry raw bytes and have their own tests below
    assert sorted(HANDLERS) == sorted([name for name, *_ in CASES] + ["upload_source", "download_artifact"])


@pytest.mark.parametrize("name,params,method,path,query,body", CASES, ids=[c[0] for c in CASES])
def test_request(name, params, method, path, query, body):
    ctx, session, _ = make_ctx(routes_for(name))
    items = run(HANDLERS[name], ctx, params)
    first = session.calls[0]
    assert first.method == method
    assert first.path == path
    assert first.headers["Authorization"] == "Bearer user:12345-test"
    if ":" in path:
        assert "%3A" in first.raw_path and ":" not in first.raw_path.split("/v1/gemini-notebook/")[1]
    for key, value in query.items():
        assert first.query.get(key) == value
    if body is not None:
        for key, value in body.items():
            assert first.body.get(key) == value, (key, first.body)
    assert outs(items, "text"), "every tool returns readable text"


def test_upload_source_sends_raw_bytes():
    class F:
        blob = b"%PDF-1.7 data"
        filename = "apollo.pdf"
        mime_type = "application/pdf"

    ctx, session, _ = make_ctx(
        [
            ("POST", "sources/upload", {"notebook": NB, "source": SRC, "title": "apollo.pdf", "status": "preparing"}),
            ("GET", f"notebooks/{NB}", {"sources": [{"source": SRC, "status": "ready"}]}),
        ]
    )
    items = run(HANDLERS["upload_source"], ctx, {"notebook": NB, "file": F()})
    call = session.calls[0]
    assert call.path == "sources/upload"
    assert call.query == {"notebook": NB, "name": "apollo.pdf"}
    assert call.data == F.blob and call.headers["Content-Type"] == "application/pdf"
    assert vars_of(items)["source_ids"] == [SRC]
    assert vars_of(items)["ready"] is True


def test_add_sources_waits_until_ready():
    ctx, session, clock = make_ctx(
        [
            ("POST", "sources", {"notebook": NB, "sources": [{"source": SRC, "status": "preparing"}]}),
            (
                "GET",
                f"notebooks/{NB}",
                [{"sources": [{"source": SRC, "status": "processing"}]}, {"sources": [{"source": SRC, "status": "ready"}]}],
            ),
        ]
    )
    items = run(HANDLERS["add_sources"], ctx, {"notebook": NB, "urls": "https://a.com"})
    assert vars_of(items)["ready"] is True
    assert len([c for c in session.calls if c.method == "GET"]) == 2
    assert clock.sleeps == [10]


def test_add_sources_requires_something():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="at least one"):
        run(HANDLERS["add_sources"], ctx, {"notebook": NB})


def test_generation_polls_and_attaches_the_file():
    ctx, session, clock = make_ctx(
        [
            ("POST", "artifacts", job(status="processing")),
            ("GET", "jobs/", [job(status="processing"), job()]),
            (
                "GET",
                "artifacts/download",
                FakeResponse(
                    200,
                    content=b"m4a-bytes",
                    headers={"Content-Type": "audio/mp4", "Content-Disposition": 'attachment; filename="Podcast.m4a"'},
                ),
            ),
        ]
    )
    items = run(HANDLERS["generate_audio_overview"], ctx, {"notebook": NB})
    v = vars_of(items)
    assert v["status"] == "completed" and v["jobid"] == JOB and v["file_urls"] == [DL]
    blobs = outs(items, "blob")
    assert blobs and blobs[0].value == b"m4a-bytes"
    assert blobs[0].meta == {"mime_type": "audio/mp4", "filename": "Podcast.m4a"}
    assert clock.sleeps == [15, 15]
    assert "Duration 4:37" in outs(items, "text")[0].value


def test_generation_still_running_after_max_wait():
    ctx, _, clock = make_ctx([("POST", "artifacts", job(status="processing")), ("GET", "jobs/", job(status="processing"))])
    items = run(HANDLERS["generate_video_overview"], ctx, {"notebook": NB, "max_wait_seconds": 40})
    assert vars_of(items)["status"] == "processing"
    assert "still generating" in outs(items, "text")[0].value
    assert sum(clock.sleeps) == 40


def test_failed_job_raises_readable_error():
    failed = job(
        status="failed", error={"code": "quota", "message": "Not enough of Google's 5h window", "retryAt": "2026-09-28T04:25:40.000Z"}
    )
    ctx, _, _ = make_ctx([("POST", "artifacts", FakeResponse(429, failed))])
    with pytest.raises(UseapiError, match="quota.*resets at 2026-09-28"):
        run(HANDLERS["generate_audio_overview"], ctx, {"notebook": NB})


def test_async_unavailable_falls_back_to_sync():
    ctx, session, _ = make_ctx(
        [("POST", "artifacts", [FakeResponse(503, {"error": "Async mode is unavailable right now, use mode sync", "code": 503}), job()])]
    )
    run(HANDLERS["generate_report"], ctx, {"notebook": NB, "return_file": False})
    assert [c.body["mode"] for c in session.calls] == ["async", "sync"]


def test_one_shot_and_default_email():
    ctx, session, _ = make_ctx([("POST", "artifacts", job())], email="me@example.com")
    run(HANDLERS["generate_audio_overview"], ctx, {"text": "Some text", "title": "Talk", "delete_notebook": True, **NOWAIT})
    body = session.calls[0].body
    assert body["text"] == "Some text" and body["title"] == "Talk" and body["email"] == "me@example.com"
    assert "deleteNotebook" not in body and "notebook" not in body


def test_generation_needs_notebook_or_sources():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="notebook id, or urls"):
        run(HANDLERS["generate_quiz"], ctx, {})


def test_video_rules():
    ctx, session, _ = make_ctx([("POST", "artifacts", job(kind="video"))])
    items = run(
        HANDLERS["generate_video_overview"], ctx, {"notebook": NB, "format": "cinematic", "style": "anime", "language": "es", **NOWAIT}
    )
    body = session.calls[0].body
    assert "style" not in body and "language" not in body
    assert any("ignored" in o.value for o in outs(items, "text"))
    ctx, session, _ = make_ctx([("POST", "artifacts", job(kind="video"))])
    run(HANDLERS["generate_video_overview"], ctx, {"notebook": NB, "style_prompt": "1960s newsreel", **NOWAIT})
    assert session.calls[0].body["style"] == "custom" and session.calls[0].body["stylePrompt"] == "1960s newsreel"
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="style prompt"):
        run(HANDLERS["generate_video_overview"], ctx, {"notebook": NB, "style": "custom"})


def test_custom_report_needs_instructions():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="needs instructions"):
        run(HANDLERS["generate_report"], ctx, {"notebook": NB, "format": "custom"})


def test_ask_notebook_outputs():
    ctx, session, _ = make_ctx(
        [
            (
                "POST",
                "chat",
                {
                    "answer": "It overshot [1].",
                    "conversation": "c9",
                    "citations": [{"number": 1, "source": SRC, "text": "Eagle passed landmarks early"}],
                },
            )
        ]
    )
    items = run(HANDLERS["ask_notebook"], ctx, {"notebook": NB, "question": "What went wrong?"})
    v = vars_of(items)
    assert v["answer"] == "It overshot [1]." and v["conversation"] == "c9"
    assert "[1] Eagle passed landmarks early" in outs(items, "text")[0].value
    assert session.calls[0].timeout >= 120


def test_download_artifact_blob_and_query():
    ctx, session, _ = make_ctx([("GET", "artifacts/download", FakeResponse(200, content=b"png", headers={"Content-Type": "image/png"}))])
    items = run(HANDLERS["download_artifact"], ctx, {"artifact": ART, "format": "slide", "index": 2, "width": 1024})
    call = session.calls[0]
    assert call.query == {"artifact": ART, "format": "slide", "index": "2", "width": "1024"}
    assert outs(items, "blob")[0].meta["mime_type"] == "image/png"


def test_download_refuses_foreign_urls():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="outside api.useapi.net"):
        ctx.client.download("https://evil.example.com/file")


def test_research_renders_report_and_sources():
    rec = job(
        kind="research",
        result={
            "mode": "deep",
            "query": "Q",
            "report": {"title": "R", "markdown": "# Report"},
            "sources": [{"url": "https://a.com", "title": "A", "cited": True}, {"url": "https://b.com", "title": "B", "cited": False}],
        },
    )
    ctx, _, _ = make_ctx([("POST", "research", rec)])
    items = run(HANDLERS["research"], ctx, {"notebook": NB, "query": "Q"})
    t = vars_of(items)["text"]
    assert "# Report" in t and "- A: https://a.com" in t and "(not cited)" in t


def test_create_note_needs_exactly_one_input():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError):
        run(HANDLERS["create_note"], ctx, {"notebook": NB, "content": "x", "conversation": "c"})


def test_share_needs_a_change():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="Nothing to change"):
        run(HANDLERS["share_notebook"], ctx, {"notebook": NB, "notify": True})


def test_required_parameter_message():
    ctx, _, _ = make_ctx()
    with pytest.raises(UseapiError, match="'question' is required"):
        run(HANDLERS["ask_notebook"], ctx, {"notebook": NB})
