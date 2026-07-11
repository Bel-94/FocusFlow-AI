"""Domain models and validation helpers for FocusFlow AI."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class PlanResult:
    """Structured productivity plan returned by Bedrock and the API."""

    priority: list[str]
    schedule: list[str]
    focus_tip: str
    motivation: str
    plan_id: str | None = None
    created_at: str | None = None

    def to_api_dict(self) -> dict[str, Any]:
        """Serialize for API responses (snake_case keys)."""
        payload: dict[str, Any] = {
            "priority": self.priority,
            "schedule": self.schedule,
            "focus_tip": self.focus_tip,
            "motivation": self.motivation,
        }
        if self.plan_id is not None:
            payload["planId"] = self.plan_id
        if self.created_at is not None:
            payload["createdAt"] = self.created_at
        return payload

    def to_dynamo_attrs(self, *, plan_id: str, tasks: str, created_at: str) -> dict[str, Any]:
        """Serialize for DynamoDB (table attribute names)."""
        return {
            "planId": plan_id,
            "tasks": tasks,
            "priority": self.priority,
            "schedule": self.schedule,
            "focusTip": self.focus_tip,
            "motivation": self.motivation,
            "createdAt": created_at,
        }


@dataclass(slots=True)
class HistoryItem:
    """A previously stored plan, including the original tasks."""

    plan_id: str
    tasks: str
    priority: list[str]
    schedule: list[str]
    focus_tip: str
    motivation: str
    created_at: str

    def to_api_dict(self) -> dict[str, Any]:
        return {
            "planId": self.plan_id,
            "tasks": self.tasks,
            "priority": self.priority,
            "schedule": self.schedule,
            "focus_tip": self.focus_tip,
            "motivation": self.motivation,
            "createdAt": self.created_at,
        }

    @classmethod
    def from_dynamo_item(cls, item: dict[str, Any]) -> HistoryItem:
        return cls(
            plan_id=str(item.get("planId", "")),
            tasks=str(item.get("tasks", "")),
            priority=_as_str_list(item.get("priority")),
            schedule=_as_str_list(item.get("schedule")),
            focus_tip=str(item.get("focusTip", "")),
            motivation=str(item.get("motivation", "")),
            created_at=str(item.get("createdAt", "")),
        )


@dataclass(slots=True)
class GeneratePlanRequest:
    """Validated inbound request for POST /generate-plan."""

    tasks: str = field(default="")


class ValidationError(ValueError):
    """Raised when request input fails validation."""


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def parse_plan_payload(data: dict[str, Any]) -> PlanResult:
    """Validate and normalize a Bedrock JSON object into PlanResult."""
    if not isinstance(data, dict):
        raise ValidationError("Plan payload must be a JSON object.")

    priority = data.get("priority")
    schedule = data.get("schedule")
    focus_tip = data.get("focus_tip", data.get("focusTip", ""))
    motivation = data.get("motivation", "")

    if not isinstance(priority, list) or not priority:
        raise ValidationError("Plan must include a non-empty 'priority' array.")
    if not isinstance(schedule, list) or not schedule:
        raise ValidationError("Plan must include a non-empty 'schedule' array.")
    if not isinstance(focus_tip, str) or not focus_tip.strip():
        raise ValidationError("Plan must include a non-empty 'focus_tip' string.")
    if not isinstance(motivation, str) or not motivation.strip():
        raise ValidationError("Plan must include a non-empty 'motivation' string.")

    return PlanResult(
        priority=[str(item).strip() for item in priority if str(item).strip()],
        schedule=[str(item).strip() for item in schedule if str(item).strip()],
        focus_tip=focus_tip.strip(),
        motivation=motivation.strip(),
    )


def plan_result_dict(plan: PlanResult) -> dict[str, Any]:
    """Convenience wrapper used in tests/logging."""
    return asdict(plan)
