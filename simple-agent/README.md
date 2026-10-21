# Simple Agent

Minimal (~15 lines) tool-calling agent implementations using Gemini.

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
