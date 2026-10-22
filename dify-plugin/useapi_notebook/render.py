"""Readable text for finished Gemini Notebook (NotebookLM) results, so an agent
or a workflow's next LLM node can use them without parsing JSON."""

from __future__ import annotations

from typing import Any


def _table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""

    def cell(value: Any) -> str:
        return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")

    width = max(len(r) for r in rows)
    padded = [list(r) + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(cell(c) for c in padded[0]) + " |", "|" + "---|" * width]
    lines += ["| " + " | ".join(cell(c) for c in r) + " |" for r in padded[1:]]
    return "\n".join(lines)


def _quiz(content: Any) -> str:
    questions = content.get("quiz", []) if isinstance(content, dict) else []
    out: list[str] = []
    for n, q in enumerate(questions, 1):
        if not isinstance(q, dict):
            continue
        out.append(f"{n}. {q.get('question', '')}")
        for i, option in enumerate(q.get("answerOptions") or []):
            mark = " (correct)" if option.get("isCorrect") else ""
            out.append(f"   {chr(65 + i)}. {option.get('text', '')}{mark}")
        if q.get("hint"):
            out.append(f"   Hint: {q['hint']}")
    return "\n".join(out)


def _flashcards(content: Any) -> str:
    cards = content.get("flashcards", []) if isinstance(content, dict) else []
    out: list[str] = []
    for n, card in enumerate(cards, 1):
        if isinstance(card, dict):
            values = [str(v) for v in card.values() if isinstance(v, (str, int, float))]
            out.append(f"{n}. " + " | ".join(values))
        else:
            out.append(f"{n}. {card}")
    return "\n".join(out)


def _mindmap(node: Any, depth: int = 0) -> list[str]:
    if not isinstance(node, dict):
        return []
    lines = ["  " * depth + "- " + str(node.get("name", ""))] if node.get("name") else []
    for child in node.get("children") or []:
        lines += _mindmap(child, depth + (1 if lines else 0))
    return lines


def _research(result: dict[str, Any]) -> str:
    parts: list[str] = []
    report = result.get("report") or {}
    if report.get("markdown"):
        parts.append(report["markdown"])
    elif result.get("summary"):
        parts.append(result["summary"])
    if result.get("noResults"):
        parts.append("The research found no sources.")
    sources = result.get("sources") or []
    if sources:
        parts.append("Sources:")
        parts += [
            f"- {s.get('title')}: {s.get('url')}" + ("" if s.get("cited", True) else " (not cited)") for s in sources if isinstance(s, dict)
        ]
    return "\n".join(parts)


def render_result(kind: str | None, result: dict[str, Any] | None) -> str:
    if not isinstance(result, dict):
        return ""
    if kind == "research" or ("query" in result and "sources" in result):
        return _research(result)
    if kind == "table":
        return _table(result.get("table") or [])
    if kind == "quiz":
        return _quiz(result.get("content"))
    if kind == "flashcards":
        return _flashcards(result.get("content"))
    if kind == "mindmap":
        return "\n".join(_mindmap(result.get("content")))
    if kind == "slides":
        slides = result.get("slides") or []
        lines = [f"Slide {i}: {s.get('caption') or ''} {s.get('text') or ''}".strip() for i, s in enumerate(slides, 1)]
        return "\n".join(lines)
    if kind == "interactive_report":
        text = result.get("text") or ""
        embedded = result.get("embedded") or []
        if embedded:
            text += "\n\nSuggested items (generate with 'Generate a suggested item'):\n"
            text += "\n".join(f"- {e.get('type')}: {e.get('title')} id: {e.get('artifact')}" for e in embedded)
        return text
    return result.get("text") or ""


def summarize_job(job: dict[str, Any]) -> str:
    result = job.get("result") if isinstance(job.get("result"), dict) else {}
    kind = job.get("type")
    title = result.get("title") or (result.get("report") or {}).get("title") or ""
    line = f"The {kind} job completed" + (f": '{title}'" if title else "") + "."
    if result.get("duration"):
        minutes, seconds = divmod(int(result["duration"]), 60)
        line += f" Duration {minutes}:{seconds:02d}."
    files = result.get("files") or []
    if files:
        line += " Files: " + ", ".join(str(f.get("format")) for f in files) + "."
    line += f" notebook: {job.get('notebook')}"
    if job.get("artifact"):
        line += f" artifact: {job.get('artifact')}"
    return line
