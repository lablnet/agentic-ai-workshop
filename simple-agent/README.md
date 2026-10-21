# Simple Agent

Minimal (~15 lines) tool-calling agent implementations using Gemini.

## Files

- [agent_with_langgraph.py](file:///Users/lablnet/projects/lablnet/seminar/multi-tool-rag-agent/simple-agent/agent_with_langgraph.py): Minimal agent using LangGraph (`create_react_agent`).
- [agent_without_langgraph.py](file:///Users/lablnet/projects/lablnet/seminar/multi-tool-rag-agent/simple-agent/agent_without_langgraph.py): Minimal agent using Gemini SDK automatic function calling.
- [helper.py](file:///Users/lablnet/projects/lablnet/seminar/multi-tool-rag-agent/simple-agent/helper.py): Shared tool function (`get_crypto_price`).

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
