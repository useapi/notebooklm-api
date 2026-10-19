"""Dify's agent runtime treats a variable (or text) message with an empty value as a
tool invoke error, so no tool may emit one in any path."""

from __future__ import annotations

import pytest
from test_tools import ART, CASES, DL, JOB, NB, job

from fakes import FakeResponse, make_ctx
from useapi_notebook import runner
from useapi_notebook.client import UseapiError
from useapi_notebook.handlers import HANDLERS

GENERATORS = [n for n in HANDLERS if n.startswith("generate_")] + ["research", "retry_artifact", "revise_slide", "get_job"]

EMPTY_RESULTS = {
    "completed_no_text": job(result={"title": "", "files": []}),
    "completed_audio": job(),
    "completed_empty_result": job(result={}),
    "running": job(status="processing", artifact=None),
    "pending_no_artifact": job(status="pending", artifact=None),
}


def assert_clean(items):
    for out in items:
        if out.kind in ("var", "text", "link"):
            assert not runner.is_empty(out.value), out
        if out.kind == "json":
            assert out.value not in ({}, [], None), out
    texts = [o for o in items if o.kind == "text"]
    assert texts and texts[0].value.strip(), "a non-empty text comes first for agents"


def params_for(name):
    base = {"wait": True, "max_wait_seconds": 30}
    if name == "get_job":
        return {**base, "jobid": JOB}
    if name in ("retry_artifact",):
        return {**base, "artifact": ART}
    if name == "revise_slide":
        return {**base, "artifact": ART, "slide": 1, "prompt": "x"}
    if name == "generate_suggested_item":
        return {**base, "artifact": ART}
    if name == "research":
        return {**base, "notebook": NB, "query": "q"}
    return {**base, "notebook": NB}


@pytest.mark.parametrize("state", list(EMPTY_RESULTS))
@pytest.mark.parametrize("name", GENERATORS)
def test_job_tools_never_emit_empty(name, state):
    record = EMPTY_RESULTS[state]
    ctx, _, _ = make_ctx(
        [
            ("POST", "", record),
            ("GET", "jobs/", record),
            ("GET", "artifacts/download", FakeResponse(200, content=b"x", headers={"Content-Type": "audio/mp4"})),
        ]
    )
    items = list(runner.outputs(ctx, name, params_for(name)))
    assert_clean(items)
    if record["status"] in ("pending", "processing"):
        first = items[0].value
        assert JOB in first and "get_job" in first and "wait=true" in first
        assert any(o.kind == "var" and o.name == "jobid" and o.value == JOB for o in items)


@pytest.mark.parametrize("name", GENERATORS)
def test_failed_job_raises_not_empty(name):
    record = job(status="failed", error={"code": "generation_failed", "message": "Google reported the generation as failed"})
    ctx, _, _ = make_ctx([("POST", "", record), ("GET", "jobs/", record)])
    with pytest.raises(UseapiError, match="generation_failed"):
        list(runner.outputs(ctx, name, params_for(name)))


@pytest.mark.parametrize("name,params", [(c[0], c[1]) for c in CASES], ids=[c[0] for c in CASES])
def test_every_tool_with_empty_api_answers(name, params):
    """Even when the API answers {} everywhere, nothing empty reaches Dify."""
    ctx, _, _ = make_ctx(
        [
            ("GET", "jobs/", job(status="processing")),
            ("POST", "artifacts", job(status="processing")),
            ("POST", "research", job(kind="research", status="processing")),
        ]
    )
    try:
        items = list(runner.outputs(ctx, name, params))
    except UseapiError as e:  # a readable error is fine; an empty message is not
        assert str(e).strip()
        return
    assert_clean(items)


def test_running_job_stops_at_the_default_wait():
    ctx, _, clock = make_ctx([("POST", "artifacts", job(status="processing")), ("GET", "jobs/", job(status="processing"))])
    list(runner.outputs(ctx, "generate_audio_overview", {"notebook": NB}))
    assert sum(clock.sleeps) == 120


def test_completed_audio_without_text_still_has_file_and_vars():
    ctx, _, _ = make_ctx(
        [
            ("POST", "artifacts", job()),
            ("GET", "artifacts/download", FakeResponse(200, content=b"m4a", headers={"Content-Type": "audio/mp4"})),
        ]
    )
    items = list(runner.outputs(ctx, "generate_audio_overview", {"notebook": NB}))
    names = {o.name for o in items if o.kind == "var"}
    assert "text" not in names and {"jobid", "status", "file_urls", "title"} <= names
    assert any(o.kind == "blob" for o in items)
    assert DL in [o.value for o in items if o.kind == "var" and o.name == "file_urls"][0]
