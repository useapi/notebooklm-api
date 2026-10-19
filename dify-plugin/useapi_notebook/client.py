"""HTTP client for the useapi.net Gemini Notebook API (NotebookLM).

Every request goes to https://api.useapi.net/v1/gemini-notebook with the
user's useapi.net API token as a Bearer token. Nothing else is contacted.
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import quote

import requests

BASE_URL = "https://api.useapi.net/v1/gemini-notebook"
USER_AGENT = "dify-plugin-notebooklm-useapi/0.1.1"

SETUP_TOKEN_URL = "https://useapi.net/docs/start-here/setup-useapi"
SETUP_ACCOUNT_URL = "https://useapi.net/docs/start-here/setup-gemini-notebook"
SUBSCRIPTION_URL = "https://useapi.net/docs/subscription"

# Seconds. Chat waits up to 120 s on the server, so its client timeout is longer.
DEFAULT_TIMEOUT = 60
CHAT_TIMEOUT = 150
DOWNLOAD_TIMEOUT = 300
UPLOAD_TIMEOUT = 300


class UseapiError(Exception):
    """A readable error for the Dify user or agent."""

    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


def enc(value: str) -> str:
    """URL-encode an id for use in a path. Ids contain ':' and '@'."""
    return quote(str(value), safe="")


def _server_message(body: Any) -> str:
    if isinstance(body, dict):
        err = body.get("error")
        if isinstance(err, dict):
            code = err.get("code")
            msg = err.get("message") or ""
            return f"{code}: {msg}" if code else msg
        if err:
            return str(err)
    if isinstance(body, str):
        return body.strip()[:500]
    return ""


def describe_error(status: int, body: Any) -> str:
    """Turn an HTTP error from the API into one readable sentence or two."""
    server = _server_message(body)
    detail = f" Details: {server}" if server else ""
    retry_at = body.get("retryAt") if isinstance(body, dict) else None

    if status == 401:
        return (
            "useapi.net rejected the API token (401 Unauthorized). Check the token in the "
            f"plugin's credentials. How to get one: {SETUP_TOKEN_URL}"
        )
    if status == 402:
        return (
            "Your useapi.net subscription has expired or does not cover this request "
            f"(402 Payment Required). See {SUBSCRIPTION_URL}.{detail}"
        )
    if status == 403:
        return f"Forbidden (403): the id belongs to a different API token, or Google does not allow this on the account's plan.{detail}"
    if status == 404:
        hint = ""
        if "not configured" in server or (server.startswith("Account ") and "not found" in server):
            hint = f" Connect the Google account first: {SETUP_ACCOUNT_URL}"
        return f"Not found (404).{detail}{hint}"
    if status == 409:
        return (
            "The notebook or item is not in the right state yet (409), for example its "
            f"sources are still processing. Wait a little and try again.{detail}"
        )
    if status == 411:
        return "The upload was refused because its size is unknown (411)."
    if status == 413:
        return "The file is too large (413). The API accepts files up to 200 MB."
    if status == 422:
        return f"Google could not do this (422).{detail}"
    if status == 429:
        when = f" Usage resets at {retry_at}." if retry_at else ""
        return f"The Google account is busy or out of NotebookLM usage right now (429).{when} Connect more accounts or try later.{detail}"
    if status == 596:
        return (
            "Google signed this account out (596). Retry in about a minute; if it persists, "
            f"re-add the account at {SETUP_ACCOUNT_URL}.{detail}"
        )
    if status == 504:
        return f"Google did not answer in time (504). It may still finish: check before retrying anything that creates content.{detail}"
    if status >= 500:
        return f"NotebookLM (Gemini Notebook) is temporarily unavailable ({status}). Retry in a few minutes.{detail}"
    return f"Request failed ({status}).{detail}"


def _parse_body(resp: requests.Response) -> Any:
    text = resp.text
    if not text:
        return None
    try:
        return resp.json()
    except ValueError:
        return text


class Client:
    def __init__(self, token: str, session: requests.Session | None = None, base_url: str = BASE_URL):
        token = (token or "").strip()
        if not token:
            raise UseapiError(f"The useapi.net API token is missing. How to get one: {SETUP_TOKEN_URL}")
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.http = session or requests.Session()

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if extra:
            headers.update(extra)
        return headers

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        data: bytes | None = None,
        content_type: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        ok_job_record: bool = False,
    ) -> Any:
        """Send one request and return the parsed JSON body.

        ok_job_record: a sync-mode generation that fails answers with an error
        status and the failed job record as its body. When set, such a body is
        returned instead of raised, so the caller can report the job.
        """
        extra: dict[str, str] = {}
        payload: bytes | None = None
        if body is not None:
            extra["Content-Type"] = "application/json"
            payload = json.dumps(body).encode("utf-8")
        elif data is not None:
            extra["Content-Type"] = content_type or "application/octet-stream"
            payload = data
        clean_params = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        try:
            resp = self.http.request(
                method,
                self.url(path),
                params=clean_params or None,
                data=payload,
                headers=self._headers(extra),
                timeout=timeout,
            )
        except requests.Timeout as e:
            raise UseapiError(
                f"No answer from api.useapi.net within {int(timeout)} seconds. "
                "The request may still complete: check before retrying anything that creates content."
            ) from e
        except requests.RequestException as e:
            raise UseapiError(f"Could not reach api.useapi.net: {e.__class__.__name__}") from e

        parsed = _parse_body(resp)
        if resp.status_code < 400:
            return parsed if parsed is not None else {}
        if ok_job_record and isinstance(parsed, dict) and parsed.get("jobid"):
            return parsed
        raise UseapiError(describe_error(resp.status_code, parsed), resp.status_code, parsed)

    def download(self, url: str, timeout: float = DOWNLOAD_TIMEOUT, max_bytes: int | None = None) -> tuple[bytes, str, str | None]:
        """Download a GET /artifacts/download link. Returns (bytes, content type, file name)."""
        if not url.startswith(self.base_url + "/"):
            raise UseapiError("Refusing to download a file from outside api.useapi.net.")
        try:
            resp = self.http.get(url, headers=self._headers({"Accept": "*/*"}), timeout=timeout, stream=True)
        except requests.Timeout as e:
            raise UseapiError(f"The file download did not finish within {int(timeout)} seconds.") from e
        except requests.RequestException as e:
            raise UseapiError(f"Could not reach api.useapi.net: {e.__class__.__name__}") from e
        if resp.status_code >= 400:
            raise UseapiError(describe_error(resp.status_code, _parse_body(resp)), resp.status_code)
        length = resp.headers.get("Content-Length")
        if max_bytes and length and length.isdigit() and int(length) > max_bytes:
            resp.close()
            raise FileTooLarge(int(length))
        chunks: list[bytes] = []
        total = 0
        for chunk in resp.iter_content(chunk_size=1 << 16):
            total += len(chunk)
            if max_bytes and total > max_bytes:
                resp.close()
                raise FileTooLarge(total)
            chunks.append(chunk)
        content_type = resp.headers.get("Content-Type", "application/octet-stream").split(";")[0].strip()
        return b"".join(chunks), content_type, _filename(resp.headers.get("Content-Disposition"))


class FileTooLarge(Exception):
    def __init__(self, size: int):
        super().__init__(size)
        self.size = size


def _filename(disposition: str | None) -> str | None:
    if not disposition or "filename=" not in disposition:
        return None
    name = disposition.split("filename=", 1)[1].split(";")[0].strip().strip('"')
    return name or None
