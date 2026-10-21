# Shared tools

Setup, run commands, and import examples are in the [root README](../README.md#shared-tools-and-project-layout).

These are ordinary Python functions with type hints and docstrings. LangChain and Gemini derive their tool schemas automatically, without `@tool` decorators.

| File | Function | Purpose |
| --- | --- | --- |
| `main.py` | `ALL_TOOLS` and individual exports | Collect the shared functions |
| `weather.py` | `get_weather(location)` | Current weather from Open-Meteo |
| `crypto.py` | `get_crypto_price(coin)` | Current USD price from CoinGecko |
| `maths.py` | `calculate(a, b, operation)` | Basic arithmetic |
| `knowledge_base.py` | `search_in_knowledge_base(query)` | Search saved HEC document embeddings |

Importing the package does not call APIs or load the knowledge base. RAG libraries and saved embeddings load only when search is called. The embedding file is located relative to the repository, independent of the working directory.
