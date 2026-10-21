"""Draft an announcement, pause for human review, then save only if approved."""

import argparse
import logging
import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command

from workflow import build_workflow


def ask_for_review():
    while True:
        action = input("Choose approve / edit / reject: ").strip().lower()
        if action == "edit":
            print("Enter the replacement announcement. Finish with a line containing only END.")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            edited = "\n".join(lines).strip()
            if not edited:
                print("The edited announcement cannot be empty.")
                continue
            print("\nYour replacement:\n" + edited)
            if input("Approve this version? Type yes: ").strip().lower() == "yes":
                return {"action": "edit", "draft": edited}
        elif action in {"approve", "reject"}:
            return {"action": action}
        else:
            print("Please choose approve, edit, or reject.")


def main():
    folder = Path(__file__).resolve().parent
    load_dotenv(folder.parent / ".env", override=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="?", default=
                        "Announce an AI agents seminar on 28 October 2026 at 10 AM in Room 101.")
    args = parser.parse_args()
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )
    graph = build_workflow(model, folder / "data")
    run_id = uuid4().hex
    config = {"configurable": {"thread_id": run_id}}
    result = graph.invoke({"request": args.request, "run_id": run_id,
                           "draft": "", "approved": False, "saved_path": ""}, config=config)
    if result.get("__interrupt__"):
        print("\nPAUSED FOR REVIEW\n\n" + result["__interrupt__"][0].value["draft"] + "\n")
        result = graph.invoke(Command(resume=ask_for_review()), config=config)
    print(f"\nSaved: {result['saved_path']}" if result["approved"] else "\nRejected. No announcement saved.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nReview cancelled. No announcement saved.")
