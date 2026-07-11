"""HTTP client for the FocusFlow AI API Gateway."""

from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_TIMEOUT_SECONDS = 45


class ApiError(Exception):
    """Raised when the FocusFlow API returns an error or is unreachable."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def get_api_base_url() -> str:
    """Resolve API base URL from environment or Streamlit secrets."""
    env_url = os.environ.get("API_BASE_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")

    try:
        import streamlit as st

        secrets_url = str(st.secrets.get("API_BASE_URL", "")).strip()
        if secrets_url:
            return secrets_url.rstrip("/")
    except Exception:
        # Secrets file may be absent during local bootstrap.
        pass

    return ""


def _headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    api_key = os.environ.get("API_KEY", "").strip()
    if not api_key:
        try:
            import streamlit as st

            api_key = str(st.secrets.get("API_KEY", "")).strip()
        except Exception:
            api_key = ""
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def generate_plan(tasks: str, *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Call POST /generate-plan and return the plan payload."""
    base_url = get_api_base_url()
    if not base_url:
        raise ApiError(
            "API_BASE_URL is not configured. Set it as an environment variable "
            "or in .streamlit/secrets.toml."
        )

    url = f"{base_url}/generate-plan"
    try:
        response = requests.post(
            url,
            json={"tasks": tasks},
            headers=_headers(),
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise ApiError("The request timed out. Please try again.") from exc
    except requests.RequestException as exc:
        raise ApiError(f"Could not reach the API: {exc}") from exc

    return _parse_response(response)


def fetch_history(*, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> list[dict[str, Any]]:
    """Call GET /history and return the plans list."""
    base_url = get_api_base_url()
    if not base_url:
        raise ApiError(
            "API_BASE_URL is not configured. Set it as an environment variable "
            "or in .streamlit/secrets.toml."
        )

    url = f"{base_url}/history"
    try:
        response = requests.get(url, headers=_headers(), timeout=timeout)
    except requests.Timeout as exc:
        raise ApiError("The history request timed out. Please try again.") from exc
    except requests.RequestException as exc:
        raise ApiError(f"Could not reach the API: {exc}") from exc

    payload = _parse_response(response)
    plans = payload.get("plans", [])
    if not isinstance(plans, list):
        raise ApiError("History response was malformed.")
    return plans


def _parse_response(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise ApiError(
            "The API returned a non-JSON response.",
            status_code=response.status_code,
        ) from exc

    if response.status_code >= 400:
        message = "Request failed."
        if isinstance(payload, dict):
            message = str(payload.get("error") or payload.get("message") or message)
        raise ApiError(message, status_code=response.status_code)

    if not isinstance(payload, dict):
        raise ApiError("Unexpected API response shape.")
    return payload
