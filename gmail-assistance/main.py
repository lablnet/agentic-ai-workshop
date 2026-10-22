"""Scaffold: watch real Gmail messages and call your live-coded email agent."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from lib.gmail_auth import connect_gmail
from lib.watcher import watch_inbox


def main():
    folder = Path(__file__).resolve().parent
    load_dotenv(folder.parent / ".env", override=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--auth-only", action="store_true", help="Authorize Gmail without running the agent")
    parser.add_argument("--interval", type=int, default=10, help="Seconds between inbox checks")
    args = parser.parse_args()
    if args.auth_only:
        from auth import main as authorize
        authorize()
        return
    if args.interval < 2:
        parser.error("--interval must be at least 2 seconds.")
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google_genai.models").setLevel(logging.WARNING)
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )
    service = connect_gmail(folder)
    owner = service.users().getProfile(userId="me").execute()["emailAddress"]
    logging.info("CONNECTED | %s", owner)
    # The watcher binds a fresh pair of Gmail tools and builds an agent per email.
    watch_inbox(service, model, owner, folder, args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nWatcher stopped.")
    except NotImplementedError as error:
        raise SystemExit(f"LIVE-CODING TODO | {error}") from None
