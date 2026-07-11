"""FocusFlow AI Lambda entrypoint.

Routes:
  POST /generate-plan  — generate and store a productivity plan
  GET  /history        — return recent plans from DynamoDB
"""

from __future__ import annotations

import logging
from typing import Any

from bedrock import BedrockClient, BedrockError
from dynamodb import DynamoDBError, PlanRepository
from models import ValidationError
from utils import (
    api_response,
    error_response,
    get_env_int,
    log_event,
    parse_json_body,
    route_key,
)

logger = logging.getLogger("focusflow")

_bedrock: BedrockClient | None = None
_repo: PlanRepository | None = None


def _get_bedrock() -> BedrockClient:
    global _bedrock
    if _bedrock is None:
        _bedrock = BedrockClient()
    return _bedrock


def _get_repo() -> PlanRepository:
    global _repo
    if _repo is None:
        _repo = PlanRepository()
    return _repo


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """API Gateway HTTP API handler (payload format 2.0)."""
    key = route_key(event)
    request_id = getattr(context, "aws_request_id", "local")

    log_event(
        logging.INFO,
        "request_received",
        route_key=key,
        request_id=request_id,
    )

    try:
        if key == "POST /generate-plan":
            return handle_generate_plan(event)
        if key == "GET /history":
            return handle_history()
        return error_response(404, f"Route not found: {key}")
    except Exception as exc:  # noqa: BLE001 — last-resort guard for API stability
        log_event(
            logging.ERROR,
            "unhandled_error",
            error=str(exc),
            route_key=key,
            request_id=request_id,
        )
        return error_response(500, "Internal server error.")


def handle_generate_plan(event: dict[str, Any]) -> dict[str, Any]:
    """Validate input, call Bedrock, persist, and return the plan."""
    try:
        body = parse_json_body(event)
    except ValueError as exc:
        return error_response(400, str(exc))

    tasks = body.get("tasks", "")
    if not isinstance(tasks, str):
        return error_response(400, "'tasks' must be a string.")

    tasks = tasks.strip()
    if not tasks:
        return error_response(400, "'tasks' must not be empty.")

    max_chars = get_env_int("MAX_TASKS_CHARS", 4000)
    if len(tasks) > max_chars:
        return error_response(
            400,
            f"'tasks' exceeds maximum length of {max_chars} characters.",
            max_tasks_chars=max_chars,
        )

    try:
        plan = _get_bedrock().generate_plan(tasks)
    except BedrockError as exc:
        return error_response(502, str(exc))

    try:
        plan = _get_repo().save_plan(tasks, plan)
    except DynamoDBError as exc:
        # Generation succeeded — return the plan and surface a persistence warning.
        log_event(logging.ERROR, "persist_degraded", error=str(exc))
        payload = plan.to_api_dict()
        payload["warning"] = "Plan generated but not saved to history."
        return api_response(200, payload)

    log_event(
        logging.INFO,
        "generate_plan_success",
        plan_id=plan.plan_id,
        priority_count=len(plan.priority),
    )
    return api_response(200, plan.to_api_dict())


def handle_history() -> dict[str, Any]:
    """Return recent plans for the History page."""
    try:
        plans = _get_repo().list_recent_plans()
    except DynamoDBError as exc:
        return error_response(500, str(exc))

    return api_response(
        200,
        {"plans": [item.to_api_dict() for item in plans]},
    )
