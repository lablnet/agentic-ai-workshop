# AI Agent Seminar Examples

Simple Python examples for a university seminar: tool calling, multi-agent collaboration, event-driven automation, guardrails, human approval, conversation memory, and retrieval-augmented generation (RAG). Gemini provides the language model; tools are shared plain Python functions.

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

## Run the guardrails agent

```bash
python3 guardrails-agent/agent.py
python3 guardrails-agent/agent.py "What is the prerequisite for CS301?"
python3 guardrails-agent/agent.py "My email is student@example.com and phone is +92 300 1234567. Can I take CS201?"
python3 guardrails-agent/agent.py "What is Bitcoin's price?"
```

The assistant answers course questions using a fictional three-course catalogue. The contact-details example demonstrates redaction before Gemini sees the question. The Bitcoin question should be rejected by the model-based scope check. Logs show input, scope, and output checks; a rejected request exits with code 1.

An allowed question uses two Gemini calls: a scope decision, then a structured answer. The output must contain nonempty `answer` and `next_step` fields, pass length limits, and contain no contact details matching the demo patterns. Scope checks can make mistakes, regexes do not detect every form of personal data, and format validation does not verify factual accuracy. See the [guardrails walkthrough](guardrails-agent/README.md).

## Run the human-in-the-loop agent

```bash
python3 human-in-the-loop-agent/agent.py
python3 human-in-the-loop-agent/agent.py "Draft an announcement for a Python workshop on 29 October 2026 at 2 PM in Lab 2."
```

Gemini drafts an announcement, then LangGraph pauses with `interrupt()`. The terminal displays the draft and offers three choices:

- `approve`: resume the graph and save the displayed draft.
- `edit`: enter a replacement over multiple lines, finish with `END`, then type `yes` to approve that version.
- `reject`: resume the graph and stop without saving an announcement.

Approved versions are saved to unique Markdown files under `human-in-the-loop-agent/data/`. Nothing is sent or published. Try separate runs with approval, editing, and rejection to demonstrate each route. Ctrl+C cancels the review.

The example uses an in-memory checkpoint and the same thread ID to pause and resume within one process. Closing the process loses its checkpoint. See the [approval workflow walkthrough](human-in-the-loop-agent/README.md).

## Run the memory agent

```bash
python3 memory-agent/agent.py
# Or choose the starting thread:
python3 memory-agent/agent.py --thread student-a
```

The agent remembers messages within each conversation thread. Try this sequence in one running session:

```text
You [demo]: My name is Ali, and I prefer Python examples.
You [demo]: Explain recursion briefly using my preferred language.
You [demo]: What is my name?
You [demo]: /history
You [demo]: /thread other
You [other]: What is my name?
You [other]: /thread demo
You [demo]: What programming language do I prefer?
You [demo]: /quit
```

In `demo`, the assistant should recall Ali and Python. In `other`, it should say it does not know the name. Switching back restores the original conversation. `/history` displays the current thread's saved messages without making a model request; each normal message makes a Gemini request. The terminal also shows the saved message count.

Memory is kept in RAM using LangGraph checkpointing and is lost when the program exits. It is saved conversation history, not retraining the model or persistent personal memory. See the [code walkthrough](memory-agent/README.md).

## Gmail assistance live-coding scaffold

This example includes working Gmail housekeeping and an email agent. The agent implementation is marked so you can remove it before live coding. It uses the same root `.venv` and `.env` as the other demos.

### Prepare before the workshop

```bash
python3 -m pip install -e '.[gmail]'
```

1. Create or select a Google Cloud project and enable the **Gmail API**.
2. Configure the OAuth consent screen. For a personal testing app, add the Gmail account you will use as a test user.
3. Create an OAuth client of type **Desktop app**, download its JSON, and save it as `gmail-assistance/credentials.json`.
4. Prepare login before the workshop:

```bash
python3 gmail-assistance/auth.py
```

Sign in to the intended account in the browser and grant the requested permissions. This caches `gmail-assistance/token.json` and prints the connected email address. It does not process or send email. The app requests `gmail.readonly` plus `gmail.compose`, which support reading messages and creating drafts/sending summaries. No Gmail password is stored in `.env`. See [Google's Python OAuth quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python).

### Code the agent live

The files you use for testing and live coding are:

```text
gmail-assistance/
    main.py        # Starts the application
    auth.py        # Standalone Gmail login
    agent.py       # LIVE CODING: build_email_agent() and analyze_email()
    tool.py        # Prepared Gmail draft and self-summary actions
    prompt.py      # LIVE CODING: email assistant instructions
    lib/           # OAuth, MIME parsing, polling, schemas and processed-ID tracking
```

1. `build_email_agent(model, tools)`: return `create_agent()` with `model=model`, `tools=tools`, the prompt, and `ToolStrategy(EmailAnalysis)`. The watcher supplies two bound Gmail tools for each email.
2. `analyze_email(agent, email)`: invoke the agent with the email fields and return `result["structured_response"]` as `EmailAnalysis`.

The agent only prepares structured output:

```python
summary: str
needs_reply: bool
draft_reply: str | None
```

`tool.py` creates plain-function tools: `create_reply_draft(summary, reply)` and `send_summary_to_self(summary)`. The agent chooses and invokes one tool. Gmail credentials, the original message and recipient addresses are bound in Python and are not model arguments. Tool inputs are validated before writes. Only one action attempt is permitted per email during that run, even if the model requests tools in parallel. The watcher verifies completion but does not perform a second action. No workshop lookup is involved.


### Test or demonstrate the agent

```bash
python3 gmail-assistance/main.py
```

Wait for `WATCHING`, then send a new email **from another account** with `AI-DEMO` in the subject, for example `AI-DEMO: Seminar question`. Existing matching inbox messages are skipped on the first run. On later runs, the saved processed-message list is reused, so messages arriving while the watcher was stopped can be processed too.

- If `needs_reply` is true, the app creates a Gmail reply draft. Open Gmail Drafts to review and manually send it.
- If false, it sends the summary to the authenticated account's own email address. There is no reply to the original sender.
- Both branches print the summary in the terminal. The model never selects Gmail recipients.

Try one email asking a question and one informational notice. The watcher polls every ten seconds; `--interval 5` changes that interval. Stop with Ctrl+C. Only matching inbox messages are read; unread/read status is unchanged. Attachments are not processed, and email bodies over 20,000 characters are rejected.

Processed IDs are stored in `gmail-assistance/processed.json`. Own/sent messages and assistant-generated summaries are excluded to avoid a summary loop. Successful actions are recorded immediately, before the model produces its final answer. Errors stop processing rather than silently retrying writes. If an agent finishes without calling a Gmail tool, or its final structured output differs from the action performed, the watcher reports an error. In this small demo, a crash after a successful Gmail action but before saving its processed ID can cause a duplicate on restart; check Drafts/Sent before retrying an uncertain action.

OAuth credentials, tokens, and processed IDs are Git-ignored. Message bodies are sent to Gemini when you implement the LangGraph agent. Use sample workshop emails. Do not delete the processing state casually: removing it creates a new baseline of existing matching emails.

See the [file-by-file scaffold walkthrough](gmail-assistance/README.md). Gmail reply threading follows [Google's thread requirements](https://developers.google.com/workspace/gmail/api/guides/threads).

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
guardrails-agent/            # Input checks, course scope and output validation
human-in-the-loop-agent/     # Draft, pause, human decision, then local save
memory-agent/                # Conversation history isolated by thread ID
gmail-assistance/            # Real Gmail plumbing
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
