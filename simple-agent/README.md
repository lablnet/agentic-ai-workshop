# Simple Agent

Two minimal tool-calling agents use the same plain `get_crypto_price` function from the shared `tools/` package.

- `agent_with_langgraph.py` uses `create_agent` to run the model/tool loop on LangGraph.
- `agent_without_langgraph.py` passes the function directly to the Gemini SDK.
