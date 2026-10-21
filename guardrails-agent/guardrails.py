"""Small, visible checks before and after calling the model."""

import re

from pydantic import BaseModel, ConfigDict, ValidationError


class GuardrailError(ValueError):
    """A request or answer did not pass a guardrail."""


class ScopeDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    allowed: bool


class SupportAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    answer: str
    next_step: str


def gemini_schema(model: type[BaseModel]) -> dict:
    """Send a basic API schema; enforce extra='forbid' locally after generation."""
    schema = model.model_json_schema()
    schema.pop("additionalProperties", None)
    return schema


def redact_contact_details(text: str) -> str:
    """Simple patterns for the seminar; these do not cover every form of personal data."""
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                  "[EMAIL REDACTED]", text)
    return re.sub(r"(?<!\w)\+?\d[\d ()-]{6,}\d(?!\w)", "[PHONE REDACTED]", text)


def validate_input(question: str) -> str:
    """Reject bad input and redact contact details before any model call."""
    if not question.strip():
        raise GuardrailError("The question cannot be empty.")
    if len(question) > 2000:
        raise GuardrailError("Keep the question under 2,000 characters.")
    return redact_contact_details(question.strip())


def validate_output(text: str) -> SupportAnswer:
    """Parse model JSON and enforce length and no leaked contact details."""
    try:
        result = SupportAnswer.model_validate_json(text)
    except ValidationError:
        raise GuardrailError("The model's answer did not match the required JSON format.") from None
    if not result.answer.strip() or not result.next_step.strip():
        raise GuardrailError("The answer and next_step must both contain text.")
    if len(result.answer) > 1500 or len(result.next_step) > 500:
        raise GuardrailError("The model's answer exceeded the demo's length limit.")
    combined = result.answer + "\n" + result.next_step
    if redact_contact_details(combined) != combined:
        raise GuardrailError("The model's answer contained contact details.")
    return result
