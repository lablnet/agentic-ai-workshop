import os
from dotenv import load_dotenv
from google import genai
from helper import get_crypto_price

load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"tools": [get_crypto_price]}
)

response = chat.send_message("What is the current price of Bitcoin?")
print(response.text)
