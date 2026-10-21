"""Chat with a memory agent and switch between independent conversation threads."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from memory_agent import build_memory_agent


def chat(agent, thread_id):
    print("Commands: /thread NAME, /history, /quit")
    print("Memory lasts while this program is running.\n")
    while True:
        message = input(f"You [{thread_id}]: ").strip()
        if not message:
            continue
        if message == "/quit":
            return
        if message == "/thread" or message.startswith("/thread "):
            name = message.removeprefix("/thread").strip()
            if name:
                thread_id = name
                print(f"Switched to thread: {thread_id}")
            else:
                print("Use /thread NAME to switch conversations.")
            continue

        config = {"configurable": {"thread_id": thread_id}}
        if message == "/history":
            history = agent.get_state(config).values.get("messages", [])
            if not history:
                print("No saved messages in this thread.")
            for saved in history:
                print(f"{saved.type}: {saved.text}")
            continue
        if message.startswith("/"):
            print("Commands: /thread NAME, /history, /quit")
            continue

        # Send only the new message. The checkpointer restores this thread's history.
        result = agent.invoke(
            {"messages": [{"role": "user", "content": message}]}, config=config,
        )
        print("Agent: " + result["messages"][-1].text)
        print(f"MEMORY | thread={thread_id} | saved messages={len(result['messages'])}\n")


def main():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread", default="demo", help="Starting conversation thread")
    args = parser.parse_args()
    if not args.thread.strip():
        parser.error("--thread cannot be empty.")
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.WARNING)
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )
    agent = build_memory_agent(model)
    chat(agent, args.thread.strip())


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nChat ended.")
