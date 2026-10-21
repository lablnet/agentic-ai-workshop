"""Input checks -> scope check -> support answer -> output checks."""

import logging
import os

from pydantic import ValidationError

from guardrails import (
    GuardrailError, ScopeDecision, SupportAnswer, gemini_schema, validate_input, validate_output,
)
from prompts import SCOPE_PROMPT, SUPPORT_PROMPT


def answer_question(client, question):
    """
    Run input, scope, answer, and output guardrails for one question.

    Args:
        client: Gemini client.
        question: Raw user question.

    Returns:
        Validated SupportAnswer.
    """
    # 1. Deterministic checks run before any text is sent to Gemini.
    clean_question = validate_input(question)
    logging.info("INPUT | passed%s", "; contact details redacted" if clean_question != question.strip() else "")

    # 2. A separate model call checks whether this is a course-support question.
    scope = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=clean_question,
        config={"system_instruction": SCOPE_PROMPT,
                "response_mime_type": "application/json", "response_schema": gemini_schema(ScopeDecision)},
    )
    if not scope.text:
        raise GuardrailError("The scope checker returned no decision.")
    try:
        decision = ScopeDecision.model_validate_json(scope.text)
    except ValidationError:
        raise GuardrailError("The scope checker returned an invalid decision.") from None
    if not decision.allowed:
        raise GuardrailError("This assistant only handles university course questions.")
    logging.info("SCOPE | course question allowed")

    # 3. Generate an answer, then check it independently before displaying it.
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=clean_question,
        config={"system_instruction": SUPPORT_PROMPT,
                "response_mime_type": "application/json", "response_schema": gemini_schema(SupportAnswer)},
    )
    if not response.text:
        raise GuardrailError("The assistant returned no answer.")
    result = validate_output(response.text)
    logging.info("OUTPUT | JSON format, length and contact-detail checks passed")
    return result
