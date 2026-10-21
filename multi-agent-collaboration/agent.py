"""One supervisor delegates tasks to three tool-using ReAct agents."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from crypto_agent import build_crypto_agent
from math_agent import build_math_agent
from supervisor_agent import build_supervisor_agent
from weather_agent import build_weather_agent


def run_specialist(agent, name, task):
    """
    Run a specialist agent and return the answer.

    Args:
        agent: The agent to run.
        name: The name of the agent.
        task: The task to delegate to the agent.

    Returns:
        The answer from the agent.
    """
    logging.info("Supervisor -> %s | %s", name, task)

    # Invoke the agent
    result = agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"recursion_limit": 12},
    )
    # Get the answer from the agent
    answer = result["messages"][-1].text
    # Log the answer
    logging.info("%s -> Supervisor | %s", name, answer)
    return answer


def build_team(model):
    """
    Build the team of agents.

    Args:
        model: The model to use for the agents.

    Returns:
        The supervisor agent.
    """
    # 1. Build the specialists defined in their own files.
    crypto_agent = build_crypto_agent(model)
    weather_agent = build_weather_agent(model)
    math_agent = build_math_agent(model)

    # 2. Wrap the agents as tools so the supervisor can choose whom to ask.
    def ask_crypto_agent(task: str) -> str:
        """Delegate cryptocurrency price lookups to the crypto specialist."""
        return run_specialist(crypto_agent, "Crypto agent", task)

    def ask_weather_agent(task: str) -> str:
        """Delegate current weather questions to the weather specialist."""
        return run_specialist(weather_agent, "Weather agent", task)

    def ask_math_agent(task: str) -> str:
        """Delegate arithmetic to the maths specialist. Include all required numbers."""
        return run_specialist(math_agent, "Math agent", task)

    # 3. The supervisor is also a ReAct agent. Its tools are other agents.
    return build_supervisor_agent(
        # The supervisor agent is also a ReAct agent. Its tools are other agents.
        model, [ask_crypto_agent, ask_weather_agent, ask_math_agent],
    )


def main():
    # Get the folder of the current file
    folder = Path(__file__).resolve().parent
    # Load the environment variables
    load_dotenv(folder.parent / ".env", override=True)
    # Create the parser
    parser = argparse.ArgumentParser(description=__doc__)
    # Add the question argument
    parser.add_argument("question", nargs="?", default=
                        "What is the current Bitcoin price in USD, and how much would 0.1 BTC cost?")
    args = parser.parse_args()
    # Check if the GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    # Configure the logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s",
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(folder / "collaboration.log", mode="w")])
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Initialize the model
    # The model is a Google Generative AI model.
    # max_retries is the number of times to retry the request if it fails.
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )

    # Build the team of agents
    supervisor = build_team(model)
    # Log the question to the supervisor
    logging.info("User -> Supervisor | %s", args.question)
    # Invoke the supervisor
    result = supervisor.invoke(
        {"messages": [{"role": "user", "content": args.question}]},
        config={"recursion_limit": 16},
    )
    # Get the answer from the supervisor
    answer = result["messages"][-1].text
    # Log the answer to the user
    logging.info("Supervisor -> User | %s", answer)
    (folder / "answer.md").write_text(answer + "\n", encoding="utf-8")
    print("\nFINAL ANSWER\n" + answer)


if __name__ == "__main__":
    main()
