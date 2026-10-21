"""Chat with a memory agent and switch between independent conversation threads."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from memory_agent import build_memory_agent


def chat(agent, thread_id):
    """
    Chat with a memory agent and switch between independent conversation threads.

    Args:
        agent: The agent to chat with.
        thread_id: The ID of the thread to chat with.
    """
    print("Commands: /thread NAME, /history, /quit")
    print("Memory lasts while this program is running.\n")
    # While the program is running, chat with the agent.
    while True:
        message = input(f"You [{thread_id}]: ").strip()
        # If the message is empty, continue.
        if not message:
            continue
        if message == "/quit":
            # If the message is /quit, return.
            return
        # If the message is /thread or /thread NAME, switch the thread.
        if message == "/thread" or message.startswith("/thread "):
            # If the message is /thread or /thread NAME, switch the thread.
            name = message.removeprefix("/thread").strip()
            if name:
                # If the name is not empty, switch the thread.
                thread_id = name
                print(f"Switched to thread: {thread_id}")
            else:
                print("Use /thread NAME to switch conversations.")
            continue

        # Configure the agent to use the thread ID.
        config = {"configurable": {"thread_id": thread_id}}
        # If the message is /history, get the history of the thread.
        if message == "/history":
            # Get the history of the thread.
            history = agent.get_state(config).values.get("messages", [])
            # If the history is empty, print a message.
            if not history:
                print("No saved messages in this thread.")
            # Print the history of the thread.
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
    # Load the environment variables
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)
    # Create the parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread", default="demo", help="Starting conversation thread")
    args = parser.parse_args()
    if not args.thread.strip():
        parser.error("--thread cannot be empty.")
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.WARNING)

    # Initialize the model
    # The model is a Google Generative AI model.
    # max_retries is the number of times to retry the request if it fails.
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )
    # Build the memory agent
    agent = build_memory_agent(model)
    # Chat with the agent
    chat(agent, args.thread.strip())


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nChat ended.")
