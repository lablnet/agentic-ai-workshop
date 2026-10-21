import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

from tools.main import get_crypto_price

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    config={"tools": [get_crypto_price]}
)

response = chat.send_message("What is the current price of Bitcoin?")
print(response.text)
