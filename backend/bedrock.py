"""Amazon Bedrock client for Nova Lite plan generation."""

from __future__ import annotations

import logging
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from models import PlanResult, ValidationError, parse_plan_payload
from prompt import SYSTEM_PROMPT, build_user_prompt
from utils import extract_json_object, get_env, log_event

logger = logging.getLogger("focusflow")


class BedrockError(RuntimeError):
    """Raised when Bedrock invocation or response parsing fails."""


class BedrockClient:
    """Thin wrapper around bedrock-runtime Converse API."""

    def __init__(self, model_id: str | None = None, client: Any | None = None) -> None:
        self.model_id = model_id or get_env("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
        self._client = client or boto3.client("bedrock-runtime")

    def generate_plan(self, tasks: str) -> PlanResult:
        """Invoke Bedrock and return a validated PlanResult."""
        user_prompt = build_user_prompt(tasks)

        log_event(
            logging.INFO,
            "bedrock_invoke_start",
            model_id=self.model_id,
            tasks_chars=len(tasks),
        )

        try:
            response = self._client.converse(
                modelId=self.model_id,
                system=[{"text": SYSTEM_PROMPT}],
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 1500,
                    # Slightly higher temperature so tips/motivation vary across runs.
                    "temperature": 0.55,
                    "topP": 0.9,
                },
            )
        except (ClientError, BotoCoreError) as exc:
            log_event(
                logging.ERROR,
                "bedrock_invoke_failed",
                error=str(exc),
                model_id=self.model_id,
            )
            raise BedrockError("Failed to invoke Amazon Bedrock.") from exc

        text = self._extract_text(response)
        log_event(
            logging.INFO,
            "bedrock_invoke_success",
            model_id=self.model_id,
            response_chars=len(text),
        )

        try:
            payload = extract_json_object(text)
            return parse_plan_payload(payload)
        except (ValueError, ValidationError) as exc:
            log_event(
                logging.ERROR,
                "bedrock_parse_failed",
                error=str(exc),
                preview=text[:300],
            )
            raise BedrockError("Bedrock returned an invalid plan payload.") from exc

    @staticmethod
    def _extract_text(response: dict[str, Any]) -> str:
        """Pull assistant text from a Converse response."""
        try:
            content = response["output"]["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise BedrockError("Unexpected Bedrock response shape.") from exc

        chunks: list[str] = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                chunks.append(str(block["text"]))

        text = "\n".join(chunks).strip()
        if not text:
            raise BedrockError("Bedrock returned an empty response.")
        return text
