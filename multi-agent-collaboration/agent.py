"""One supervisor delegates tasks to three tool-using ReAct agents."""

import argparse
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.main import calculate, get_crypto_price, get_weather


def run_specialist(agent, name, task):
    logging.info("Supervisor -> %s | %s", name, task)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"recursion_limit": 12},
    )
    answer = result["messages"][-1].text
    logging.info("%s -> Supervisor | %s", name, answer)
    return answer


def build_team(model):
    # 1. Each specialist is a complete ReAct agent with its own tool.
    crypto_agent = create_agent(
        model=model, tools=[get_crypto_price], name="crypto_agent",
        system_prompt="You are the crypto price specialist. Use your tool for prices. "
        "Return the coin, USD price and any API error accurately. Never invent prices.",
    )
    weather_agent = create_agent(
        model=model, tools=[get_weather], name="weather_agent",
        system_prompt="You are the weather specialist. Use your tool for current "
        "weather. Include the matched location and units. Never invent readings.",
    )
    math_agent = create_agent(
        model=model, tools=[calculate], name="math_agent",
        system_prompt="You are the maths specialist. Use calculate for arithmetic. "
        "Return the result with a short explanation. Do not invent missing inputs.",
    )

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
    return create_agent(
        model=model,
        tools=[ask_crypto_agent, ask_weather_agent, ask_math_agent],
        name="supervisor",
        system_prompt="You lead crypto, weather and maths specialists. Delegate every "
        "supported task to the relevant specialist; do not do their work yourself. "
        "Use only agents needed for the user's question. For dependent tasks, obtain "
        "the first result before delegating the next task, passing the actual numbers. "
        "For example, get a coin price before asking maths to calculate its cost. "
        "Combine the specialists' results into one concise answer. Report tool failures "
        "honestly and do not calculate with unavailable data. For unsupported requests, "
        "explain your available capabilities.",
    )


def main():
    folder = Path(__file__).resolve().parent
    load_dotenv(folder.parent / ".env", override=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="?", default=
                        "What is the current Bitcoin price in USD, and how much would 0.1 BTC cost?")
    args = parser.parse_args()
    if not os.getenv("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in the root .env file.")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s",
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(folder / "collaboration.log", mode="w")])
    logging.getLogger("httpx").setLevel(logging.WARNING)
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        google_api_key=os.environ["GEMINI_API_KEY"], max_retries=1, timeout=60,
    )
    supervisor = build_team(model)
    logging.info("User -> Supervisor | %s", args.question)
    result = supervisor.invoke(
        {"messages": [{"role": "user", "content": args.question}]},
        config={"recursion_limit": 16},
    )
    answer = result["messages"][-1].text
    logging.info("Supervisor -> User | %s", answer)
    (folder / "answer.md").write_text(answer + "\n", encoding="utf-8")
    print("\nFINAL ANSWER\n" + answer)


if __name__ == "__main__":
    main()
