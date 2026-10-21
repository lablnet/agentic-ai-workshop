import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from helper import get_crypto_price

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
agent = create_react_agent(llm, [get_crypto_price])

response = agent.invoke({"messages": [{"role": "user", "content": "What is the current price of Bitcoin?"}]})
print(response["messages"][-1].content)
