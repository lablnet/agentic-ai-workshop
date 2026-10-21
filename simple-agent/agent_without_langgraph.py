import os
from dotenv import load_dotenv
import google.generativeai as genai
from helper import get_crypto_price

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-2.5-flash", tools=[get_crypto_price])
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message("What is the current price of Bitcoin?")
print(response.text)
