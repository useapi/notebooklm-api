"""Live routing check: call every read-only tool against api.useapi.net with a
fake token. Each call must answer 401 (the route exists and checks the token),
never 404 (a wrong path) or 400 (a malformed id or parameter).

Run from the plugin folder:  python dev/routing_check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))

from endpoints import ENDPOINTS  # noqa: E402

from useapi_notebook.client import Client, UseapiError  # noqa: E402
from useapi_notebook.handlers import HANDLERS, Ctx  # noqa: E402

FAKE_TOKEN = "user:12345-glamahealthcheck"
NB = "user:12345-user@example.com-notebook:d02c903b-17f8-4241-a263-2be9e7359d55"
SRC = "user:12345-user@example.com-source:d02c903b-17f8-4241-a263-2be9e7359d55:c1182943-b7f0-4e89-82bc-8b3614cfb78f"
ART = "user:12345-user@example.com-artifact:d02c903b-17f8-4241-a263-2be9e7359d55:0c2ba8dc-47dd-474f-a19c-c06896e269fd"
JOB = "job:12597f9a-010c-4758-8e9a-b5cc17b0ccdb-user:12345-user@example.com-bot:gemini_notebook"

READ_ONLY = {
    "list_accounts": {},
    "get_account": {"email": "user@example.com"},
    "list_jobs": {},
    "get_job": {"jobid": JOB, "wait": False},
    "list_notebooks": {},
    "get_notebook": {"notebook": NB},
    "get_notebook_guide": {"notebook": NB},
    "get_sharing": {"notebook": NB},
    "get_source": {"source": SRC},
    "list_play_books": {},
    "get_chat_history": {"notebook": NB},
    "list_artifacts": {"notebook": NB},
    "get_artifact": {"artifact": ART},
    "download_artifact": {"artifact": ART, "format": "m4a"},
    "list_notes": {"notebook": NB},
    "list_labels": {"notebook": NB},
    "list_collections": {},
}


def main() -> int:
    ctx = Ctx(client=Client(FAKE_TOKEN))
    failures = 0
    for name, params in READ_ONLY.items():
        try:
            list(HANDLERS[name](ctx, params))
            status = 200
        except UseapiError as e:
            status = e.status
        ok = status == 401
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {status} {name:22} {ENDPOINTS[name]}")
    print(f"{len(READ_ONLY) - failures}/{len(READ_ONLY)} routes answered 401")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
