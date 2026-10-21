# Simple Agent

Minimal tool-calling agent implementations using Gemini.

Both examples import the same plain `get_crypto_price` function from `../tools/crypto.py`, through `tools/main.py`. No `@tool` decorator is required. The LangChain version builds a tool schema automatically; the Gemini version accepts the Python function directly.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY
   ```

## Usage

Run with LangGraph:
```bash
python agent_with_langgraph.py
```

Run without LangGraph:
```bash
python agent_without_langgraph.py
```
