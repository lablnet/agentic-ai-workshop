# Shared tools

All agent examples import their tools from this folder. These are ordinary Python functions.

```text
tools/
├── main.py            # Imports all tools and provides ALL_TOOLS
├── weather.py         # get_weather(location)
├── crypto.py          # get_crypto_price(coin="bitcoin")
├── maths.py           # calculate(a, b, operation)
└── knowledge_base.py  # search_in_knowledge_base(query)
```

Choose individual functions:

```python
from tools.main import get_crypto_price, get_weather

agent = create_agent(model=llm, tools=[get_crypto_price, get_weather])
```

Or load the full list:

```python
from tools.main import ALL_TOOLS

agent = create_agent(model=llm, tools=ALL_TOOLS)
```

The same functions work with the Gemini SDK:

```python
from tools.main import get_crypto_price

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"tools": [get_crypto_price]},
)
```
