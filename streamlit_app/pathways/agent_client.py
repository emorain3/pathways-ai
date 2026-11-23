"""Server-side Salesforce Agentforce API transport.

Secrets are read from Streamlit secrets or environment variables. No verification
or write authority is inferred from the Streamlit client: Salesforce owns both.
"""

from __future__ import annotations

import os
import time
import uuid

import requests
import streamlit as st

AGENT_API_BASE = "https://api.salesforce.com/einstein/ai-agent/v1"


class SalesforceAPIError(Exception):
    """A sanitized API failure; never includes tokens or request/response bodies."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def _get_secret(key: str) -> str:
    try:
        value = st.secrets.get(key)
    except (FileNotFoundError, KeyError):
        value = None
    value = value or os.environ.get(key)
    if not value:
        raise SalesforceAPIError(f"Missing required configuration: {key}")
    return str(value).strip()


def get_access_token(*, force_refresh: bool = False) -> str:
    # Per-visitor cache, not a globally shared Streamlit resource.
    cache = st.session_state.setdefault("_sf_oauth_cache", {})
    if (
        not force_refresh
        and cache.get("access_token")
        and time.monotonic() < cache.get("expires_at", 0)
    ):
        return cache["access_token"]

    url = f"{_get_secret('SF_MY_DOMAIN_URL').rstrip('/')}/services/oauth2/token"
    try:
        resp = requests.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": _get_secret("SF_CLIENT_ID"),
                "client_secret": _get_secret("SF_CLIENT_SECRET"),
            },
            timeout=(10, 20),
        )
    except requests.RequestException as exc:
        raise SalesforceAPIError("Salesforce OAuth request could not be completed") from exc
    if not resp.ok:
        detail = ""
        try:
            err_json = resp.json()
            err_code = err_json.get("error", "")
            err_desc = err_json.get("error_description", "")
            detail = f": {err_code} - {err_desc}".strip(" -")
        except ValueError:
            pass
        raise SalesforceAPIError(f"Salesforce OAuth request was rejected{detail}", resp.status_code)
    try:
        payload = resp.json()
        token = payload["access_token"]
        # Salesforce might omit expires_in. In that case cache for 10 minutes;
        # a 401 will still trigger a token refresh.
        ttl = max(1, min(int(payload.get("expires_in", 600)) - 60, 600))
    except (ValueError, TypeError, KeyError) as exc:
        raise SalesforceAPIError("Salesforce OAuth response was invalid") from exc

    cache["access_token"] = token
    cache["expires_at"] = time.monotonic() + ttl
    return token


def _request(method: str, url: str, *, body: dict | None = None, timeout: int = 30,
             extra_headers: dict | None = None) -> dict:
    # Retry only an explicit HTTP 401. Never automatically replay a timed-out
    # agent message or a 5xx: a Salesforce write may already have completed.
    for attempt in range(2):
        token = get_access_token(force_refresh=(attempt == 1))
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            **(extra_headers or {}),
        }
        try:
            response = requests.request(
                method, url, json=body, headers=headers, timeout=(10, timeout)
            )
        except requests.RequestException as exc:
            raise SalesforceAPIError(
                "Salesforce did not return a response; the action outcome may be unknown"
            ) from exc
        if response.status_code == 401 and attempt == 0:
            continue
        if not response.ok:
            detail = ""
            try:
                err_json = response.json()
                if isinstance(err_json, dict):
                    code = err_json.get("errorCode") or err_json.get("code") or ""
                    msg = err_json.get("message") or err_json.get("error") or ""
                    detail = f" ({code}: {msg})".strip(" :") if (code or msg) else ""
            except ValueError:
                pass
            raise SalesforceAPIError(
                f"Salesforce Agent API request failed on {method} {url}{detail}",
                response.status_code,
            )
        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError as exc:
            raise SalesforceAPIError("Salesforce Agent API returned an invalid response") from exc
    raise SalesforceAPIError("Salesforce Agent API authentication failed", 401)


def start_session() -> dict:
    agent_id = _get_secret("SF_AGENT_ID")
    my_domain = _get_secret("SF_MY_DOMAIN_URL").rstrip("/")
    external_session_key = str(uuid.uuid4())
    payload = {
        "externalSessionKey": external_session_key,
        "instanceConfig": {"endpoint": my_domain},
        "bypassUser": True,  # Use the Run As user associated with the OAuth token.
        "tz": "America/New_York",
        "variables": [
            {"name": "$Context.EndUserLanguage", "type": "Text", "value": "en_US"}
        ],
    }
    data = _request(
        "POST", f"{AGENT_API_BASE}/agents/{agent_id}/sessions", body=payload, timeout=30
    )
    session_id = data.get("sessionId")
    if not isinstance(session_id, str) or not session_id:
        raise SalesforceAPIError("Salesforce did not return a session ID")
    return {"session_id": session_id, "external_session_key": external_session_key}


def send_message(session_id: str, sequence_id: int, text: str) -> dict:
    body = {
        "message": {"sequenceId": sequence_id, "type": "Text", "text": text}
    }
    return _request(
        "POST", f"{AGENT_API_BASE}/sessions/{session_id}/messages",
        body=body, timeout=125,
    )


def end_session(session_id: str) -> None:
    if not session_id:
        return
    _request(
        "DELETE", f"{AGENT_API_BASE}/sessions/{session_id}", timeout=15,
        extra_headers={"x-session-end-reason": "UserRequest"},
    )
