"""DynamoDB persistence for FocusFlow AI plans."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from models import HistoryItem, PlanResult
from utils import get_env, get_env_int, log_event

logger = logging.getLogger("focusflow")


class DynamoDBError(RuntimeError):
    """Raised when DynamoDB operations fail."""


class PlanRepository:
    """Store and retrieve generated plans."""

    def __init__(self, table_name: str | None = None, client: Any | None = None) -> None:
        self.table_name = table_name or get_env("TABLE_NAME", "FocusPlans")
        self._client = client or boto3.resource("dynamodb")
        self._table = self._client.Table(self.table_name)
        self.history_limit = get_env_int("HISTORY_LIMIT", 20)

    def save_plan(self, tasks: str, plan: PlanResult) -> PlanResult:
        """Persist a plan and return it with planId / createdAt attached."""
        plan_id = str(uuid4())
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        item = plan.to_dynamo_attrs(plan_id=plan_id, tasks=tasks, created_at=created_at)

        try:
            self._table.put_item(Item=item)
        except (ClientError, BotoCoreError) as exc:
            log_event(
                logging.ERROR,
                "dynamodb_put_failed",
                error=str(exc),
                table=self.table_name,
                plan_id=plan_id,
            )
            raise DynamoDBError("Failed to store plan in DynamoDB.") from exc

        log_event(
            logging.INFO,
            "dynamodb_put_success",
            table=self.table_name,
            plan_id=plan_id,
        )

        plan.plan_id = plan_id
        plan.created_at = created_at
        return plan

    def list_recent_plans(self, limit: int | None = None) -> list[HistoryItem]:
        """Return recent plans sorted by createdAt descending."""
        scan_limit = limit or self.history_limit

        try:
            # Challenge scale: Scan is acceptable. Cap reads for cost control.
            response = self._table.scan(Limit=max(scan_limit * 2, scan_limit))
            items = response.get("Items", [])
        except (ClientError, BotoCoreError) as exc:
            log_event(
                logging.ERROR,
                "dynamodb_scan_failed",
                error=str(exc),
                table=self.table_name,
            )
            raise DynamoDBError("Failed to read plan history from DynamoDB.") from exc

        history = [HistoryItem.from_dynamo_item(item) for item in items]
        history.sort(key=lambda row: row.created_at, reverse=True)
        trimmed = history[:scan_limit]

        log_event(
            logging.INFO,
            "dynamodb_scan_success",
            table=self.table_name,
            returned=len(trimmed),
        )
        return trimmed
