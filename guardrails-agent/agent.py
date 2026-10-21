"""Run a small course-support assistant with visible guardrails."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from guardrails import GuardrailError
from support_agent import answer_question


def main():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default="What is the prerequisite for CS201?")
    args = parser.parse_args()
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google_genai.models").setLevel(logging.WARNING)
    with genai.Client(api_key=os.environ["GEMINI_API_KEY"]) as client:
        result = answer_question(client, args.question)
    print("\n" + result.model_dump_json(indent=2))


if __name__ == "__main__":
    try:
        main()
    except GuardrailError as error:
        raise SystemExit(f"BLOCKED | {error}") from None
    except APIError as error:
        raise SystemExit(f"Gemini API error ({error.code}): {error.message}") from None
