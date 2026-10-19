"""Error mapping and transport behaviour of the HTTP client."""

import pytest
import requests

from fakes import FakeResponse, FakeSession
from useapi_notebook.client import Client, UseapiError, describe_error


@pytest.mark.parametrize(
    "status,body,expected",
    [
        (401, {"error": "useapi.net ⁝ Unauthorized", "code": 401}, "rejected the API token"),
        (402, {"error": "Subscription expired", "code": 402}, "subscription has expired"),
        (403, {"error": "x does not belong to this API token", "code": 403}, "different API token"),
        (404, {"error": "Account user@example.com not found", "code": 404}, "Connect the Google account first"),
        (404, {"error": "Job job:x not found", "code": 404}, "Not found (404). Details: Job job:x not found"),
        (409, {"error": "The notebook has no ready sources to answer from", "code": 409}, "sources are still processing"),
        (413, None, "200 MB"),
        (422, {"error": "Google does not allow these books", "code": 422}, "Google could not do this"),
        (429, {"error": "busy", "code": 429, "retryAt": "2026-09-28T03:40:48.000Z"}, "resets at 2026-09-28T03:40:48.000Z"),
        (502, {"error": "Could not reach Gemini Notebook (HTTP 500), please retry", "code": 502}, "temporarily unavailable"),
        (503, {"error": "GOOGLE_BOT_CHECK", "code": 503}, "Retry in a few minutes"),
        (504, {"error": "chat failed: no answer within 120 s", "code": 504}, "did not answer in time"),
        (596, {"error": "Google signed this account out", "code": 596}, "re-add the account"),
    ],
)
def test_describe_error(status, body, expected):
    assert expected in describe_error(status, body)


def test_error_raised_with_status():
    session = FakeSession([("GET", "accounts", FakeResponse(401, {"error": "useapi.net ⁝ Unauthorized", "code": 401}))])
    with pytest.raises(UseapiError) as e:
        Client("bad", session=session).request("GET", "accounts")
    assert e.value.status == 401


def test_job_record_errors_can_be_returned():
    record = {"jobid": "job:x", "status": "failed", "error": {"code": "generation_failed"}}
    session = FakeSession([("POST", "artifacts", FakeResponse(422, record))])
    assert Client("t", session=session).request("POST", "artifacts", body={}, ok_job_record=True) == record


def test_missing_token():
    with pytest.raises(UseapiError, match="token is missing"):
        Client("  ")


class Boom:
    def __init__(self, exc):
        self.exc = exc

    def request(self, *a, **k):
        raise self.exc


def test_timeout_and_network_errors():
    with pytest.raises(UseapiError, match="within 60 seconds"):
        Client("t", session=Boom(requests.Timeout())).request("GET", "accounts")
    with pytest.raises(UseapiError, match="Could not reach api.useapi.net"):
        Client("t", session=Boom(requests.ConnectionError())).request("GET", "accounts")


def test_empty_params_are_dropped():
    session = FakeSession()
    Client("t", session=session).request("GET", "notebooks/", params={"email": None, "x": ""})
    assert session.calls[0].query == {}
