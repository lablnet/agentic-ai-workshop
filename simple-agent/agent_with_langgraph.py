import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools.main import get_crypto_price

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
    max_retries=3,
)
agent = create_agent(model=llm, tools=[get_crypto_price])

response = agent.invoke({"messages": [{"role": "user", "content": "What is the current price of Bitcoin?"}]})
print(response["messages"][-1].content)
