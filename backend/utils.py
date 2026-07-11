"""Shared utilities: logging, HTTP helpers, and input parsing."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any


def configure_logging() -> logging.Logger:
    """Configure and return the application logger."""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger("focusflow")

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    logger.setLevel(log_level)
    logger.propagate = False
    return logger


logger = configure_logging()


def log_event(level: int, message: str, **fields: Any) -> None:
    """Emit a structured JSON log line."""
    payload = {"message": message, **fields}
    logger.log(level, json.dumps(payload, default=str))


def get_env(name: str, default: str | None = None) -> str:
    """Read a required environment variable."""
    value = os.environ.get(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_env_int(name: str, default: int) -> int:
    """Read an integer environment variable with a default."""
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return int(raw)


def api_response(status_code: int, body: dict[str, Any] | list[Any]) -> dict[str, Any]:
    """Build an API Gateway HTTP API (payload 2.0) response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def error_response(status_code: int, message: str, **extra: Any) -> dict[str, Any]:
    """Build a consistent error payload."""
    body: dict[str, Any] = {"error": message}
    body.update(extra)
    return api_response(status_code, body)


def parse_json_body(event: dict[str, Any]) -> dict[str, Any]:
    """Parse the Lambda event body into a dictionary."""
    body = event.get("body")
    if body is None or body == "":
        return {}

    if event.get("isBase64Encoded"):
        import base64

        body = base64.b64decode(body).decode("utf-8")

    if isinstance(body, dict):
        return body

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Request body must be a JSON object.")
    return parsed


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract the first JSON object from model output (handles markdown fences)."""
    cleaned = text.strip()

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.DOTALL)
    if fenced:
        cleaned = fenced.group(1).strip()
    else:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in model response.")
        cleaned = cleaned[start : end + 1]

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("Model response was not valid JSON.") from exc

    if not isinstance(data, dict):
        raise ValueError("Model JSON must be an object.")
    return data


def route_key(event: dict[str, Any]) -> str:
    """Return the HTTP API route key, e.g. 'POST /generate-plan'."""
    return (
        event.get("routeKey")
        or event.get("requestContext", {}).get("routeKey")
        or "UNKNOWN"
    )
