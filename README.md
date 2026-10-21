# AI Agent Seminar Examples

Simple Python examples for a university seminar: tool calling, multi-agent collaboration, event-driven automation, and retrieval-augmented generation (RAG). Gemini provides the language model; tools are shared plain Python functions.

## Setup

Use Python 3.10 or newer. Run every command from the repository root. All examples share **one `.venv` and one `.env`**.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
cp .env.example .env
```

Edit the root `.env`:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey). Existing root `.env` files should be kept instead of overwritten. All examples load this root file; nested `.env` files are no longer used. The root configuration takes precedence over exported variables.

The editable install registers the shared `tools` package. No `sys.path` edits are needed, and edits to tool functions take effect without reinstalling. Activate the root environment in each new terminal:

```bash
source .venv/bin/activate
```

## Run the simple agents

With LangGraph:

```bash
python3 simple-agent/agent_with_langgraph.py
```

With the Gemini SDK directly:

```bash
python3 simple-agent/agent_without_langgraph.py
```

Both ask for Bitcoin's current price using the same function in `tools/crypto.py`. The LangGraph example uses the supported `create_agent` API. See the [code explanation](simple-agent/README.md).

## Run the collaborating agents

```bash
python3 multi-agent-collaboration/agent.py
```

A supervisor chooses among crypto, weather, and maths ReAct agents. The default question asks for Bitcoin's USD price and the cost of 0.1 BTC: the supervisor gets the price from the crypto agent, then passes that number to the maths agent.

Try different routes:

```bash
python3 multi-agent-collaboration/agent.py "What is 25 multiplied by 17?"
python3 multi-agent-collaboration/agent.py "What is the current temperature in Islamabad?"
python3 multi-agent-collaboration/agent.py "What is Ethereum's USD price, and what would 2 ETH cost?"
python3 multi-agent-collaboration/agent.py "Give me Islamabad's temperature, Bitcoin's USD price, and the cost of 0.1 BTC."
```

Follow delegation and tool calls in the terminal or `multi-agent-collaboration/collaboration.log`. The combined answer is saved to `multi-agent-collaboration/answer.md`; each run replaces those files. External data APIs can fail or rate-limit, in which case the agents should report unavailable data.

See the [architecture and seminar walkthrough](multi-agent-collaboration/README.md).

## Run the autonomous document agent

```bash
python3 autonomous-agent/agent.py
```

Leave it running. In another terminal, from the repository root, drop a sample document into its input folder:

```bash
cp autonomous-agent/example.md autonomous-agent/temp/first-document.md
```

The watcher automatically extracts the text, uses Gemini to format it as HTML, and writes `autonomous-agent/data/first-document.md.html`. Open that file in a browser. You can also copy a text-based PDF into `autonomous-agent/temp/`.

- Supports UTF-8 `.md` / `.markdown` and text-based `.pdf` files. Scanned PDFs require OCR and are not supported by this demo.
- New files wait at least two seconds to settle. Processing is sequential and uses one Gemini request per conversion.
- Unchanged files are skipped, including after restarting. Editing a source file triggers conversion again; deleting its HTML output also requests regeneration.
- Source files stay in `temp/`. A processing record is saved in `data/.processed.json`.
- Empty documents and documents over 60,000 extracted characters are rejected. Invalid files are logged and retried after a content change or watcher restart. API errors stop the watcher; fix the issue and restart.
- This converts text, not the original PDF layout or images. Check generated content for accuracy. Document text is sent to Gemini.

Change the polling interval if needed:

```bash
python3 autonomous-agent/agent.py --interval 3
```

Logs are appended to `autonomous-agent/autonomous.log`. Stop the watcher with **Ctrl+C**. See the [event loop and seminar walkthrough](autonomous-agent/README.md).

## Run the multi-tool and RAG notebooks

Use the same root environment. Install the optional notebook and retrieval dependencies:

```bash
python3 -m pip install -e '.[rag,notebooks]'
ollama pull mxbai-embed-large
jupyter lab
```

Ollama must be installed and running for knowledge-base search. Open these notebooks under `multi-tool agent/`:

- `agent.ipynb`: LangGraph agent for weather, crypto prices, and knowledge-base search.
- `gemini_agent.ipynb`: native Gemini function calling for the same tasks.
- `rag.ipynb`: process the HEC curriculum PDF and build embeddings if needed. A saved embedding file is already included.

Select the kernel belonging to the root `.venv`. Do not create a separate notebook environment. Example questions: “What's the weather in Islamabad?”, “What's Ethereum's price?”, and “What is the prerequisite for MSCS?”

## Shared tools and project layout

```text
.env                         # One API configuration for all examples
.venv/                       # One Python environment for all examples
pyproject.toml               # Shared package and dependencies
simple-agent/                # Basic tool calling, with and without LangGraph
multi-agent-collaboration/    # Supervisor + three specialist ReAct agents
autonomous-agent/
    temp/                    # Incoming PDF and Markdown files
    data/                    # Generated HTML pages and processing history
multi-tool agent/            # Multi-tool and RAG notebooks + saved embeddings
tools/
    main.py                  # Exports individual functions and ALL_TOOLS
    crypto.py                # CoinGecko prices
    weather.py               # Open-Meteo weather
    maths.py                 # Arithmetic
    knowledge_base.py        # Ollama embeddings + cosine similarity search
```

Tools use type hints and docstrings without `@tool`. LangChain and Gemini accept the functions directly. Knowledge-base libraries and saved embeddings load only when search is called. See the [shared tools explanation](tools/README.md).

Import selected tools or the complete list:

```python
from tools.main import get_crypto_price, get_weather
from tools.main import ALL_TOOLS

agent = create_agent(model=llm, tools=[get_crypto_price, get_weather])
# Or: agent = create_agent(model=llm, tools=ALL_TOOLS)
```

This repository is an educational project. It demonstrates small, readable implementations suitable for walking through during a seminar.
