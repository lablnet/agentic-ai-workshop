# Multi-Tool Agent with RAG

> **⚠️ Educational Project**: This project is created for learning and educational purposes. It demonstrates the implementation of RAG (Retrieval-Augmented Generation) systems, multi-tool AI agents.

A multi-purpose AI agent built with LangGraph and Google's Gemini AI that combines real-time data access with intelligent document search capabilities. The agent can help with weather information, cryptocurrency prices, and search through educational knowledge bases.

## Features

- 🌤️ **Weather Information**: Get current weather data for any location worldwide
- 💰 **Cryptocurrency Prices**: Check real-time prices for various cryptocurrencies
- 📚 **Knowledge Base Search**: Intelligent search through educational documents using RAG (Retrieval-Augmented Generation)
- 🧠 **Semantic Search**: Advanced vector-based search with semantic understanding
- 📄 **PDF Processing**: Extract and process text from PDF documents
- 🔍 **Intelligent Chunking**: Smart text splitting with context preservation

## Technologies Used

- **LangGraph**: For building the agent framework
- **Google Gemini AI**: As the language model
- **Ollama**: For generating embeddings and local AI capabilities
- **LangChain**: For document processing and text splitting
- **PyMuPDF (fitz)**: For PDF text extraction
- **scikit-learn**: For vector similarity calculations
- **Geopy**: For geocoding and location services
- **Open-Meteo API**: For weather data
- **CoinGecko API**: For cryptocurrency prices

## Setup

1. **Install Dependencies**:
   ```bash
   # Core dependencies
   pip install ollama PyMuPDF langchain langchain-community scikit-learn
   pip install langgraph langchain-google-genai geopy requests
   
   # Additional dependencies for Gemini function calling agent
   pip install google-generativeai python-dotenv
   ```

2. **Install Ollama**:
   - Download and install Ollama from [ollama.ai](https://ollama.ai)
   - Pull the embedding model: `ollama pull mxbai-embed-large`

3. **API Key Configuration**:
   - Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Set your api key in the .env file

4. **Initialize RAG System**:
   - Run `rag.ipynb` to process PDF documents and generate embeddings
   - This creates the knowledge base for semantic search

5. **Run the Agent**:
   - **LangGraph Agent**: Open `agent.ipynb` in Jupyter Notebook or JupyterLab and execute all cells
   - **Gemini Function Calling Agent**: Open `gemini_agent.ipynb` in Jupyter Notebook or JupyterLab and execute all cells

## Agent Implementations

### Seminar examples

- [Multi-agent collaboration](multi-agent-collaboration/README.md): a supervisor delegates to crypto, weather, and maths ReAct agents built on LangGraph, then combines their results, with visible logs.
- [Autonomous agent](autonomous-agent/README.md): watches `temp/` for PDF and Markdown files, automatically uses Gemini to convert them to HTML, and saves pages in `data/`.

Each folder contains readable Python code, API setup instructions, and a seminar walkthrough.

This project includes two different agent implementations:

### 1. LangGraph Agent (`agent.ipynb`)
- **Framework**: Uses LangGraph for agent orchestration
- **Pattern**: Implements ReAct (Reasoning and Acting) pattern
- **Features**: Multi-step reasoning, tool selection, and conversation management
- **Best for**: Complex multi-step tasks requiring reasoning chains

### 2. Gemini Function Calling Agent (`gemini_agent.ipynb`)
- **Framework**: Native Google Gemini function calling
- **Pattern**: Direct function calling without external agent frameworks
- **Features**: Simpler implementation, faster execution, built-in conversation history
- **Best for**: Direct tool usage with minimal overhead

Both agents provide the same functionality but use different approaches to demonstrate that we can build the agent without using any agentic framework like LangGraph or LangChain.

## Usage

The agents can respond to natural language queries like:

### Weather Queries
- "What's the weather in Islamabad?"
- "How's the weather in New York?"
- "Tell me the current weather in London"

### Cryptocurrency Queries
- "What's the price of Ethereum?"
- "What's the current Bitcoin price?"
- "How much is Litecoin worth?"

### Knowledge Base Queries
- "What is the prerequisite for MSCS?"
- "Tell me about computer science curriculum requirements"
- "What courses are required for software engineering?"
- "Explain the admission criteria for IT programs"

## Project Structure

- `tools/`: Shared plain Python functions for all agent examples; `tools/main.py` exports individual functions and `ALL_TOOLS`. See the [shared tools walkthrough](tools/README.md).
- `agent.ipynb`: Main notebook containing the multi-tool agent implementation using LangGraph
- `gemini_agent.ipynb`: **NEW!** Function calling agent implementation using Google Gemini AI with native function calling capabilities
- `rag.ipynb`: RAG system notebook for processing PDF documents and generating embeddings
- `rag.py`: Core RAG implementation with PDF processing, text splitting, and vector search
- `tools/weather.py`, `tools/crypto.py`, `tools/knowledge_base.py`, `tools/maths.py`: Common tool implementations used by the examples
- `prompt.py`: System prompts and instructions for the AI agents
- `hec_outline.pdf`: Educational document (Pakistan Universities curriculum outline)
- `hec_outline_embeddings.json`: Pre-generated embeddings for the knowledge base
- `README.md`: This documentation file

## Notes

### Educational Purpose
This project is designed for educational and learning purposes to demonstrate:
- Implementation of RAG (Retrieval-Augmented Generation) systems
- Multi-tool AI agent development using LangGraph
- Integration of various APIs and AI services
- Document processing and vector search techniques
- Best practices in AI application development

### Technical Implementation
- The agent uses a ReAct (Reasoning and Acting) pattern for tool selection
- Weather data is provided by Open-Meteo API (free tier)
- Cryptocurrency prices are fetched from CoinGecko API
- The agent includes error handling for API failures and invalid inputs

### RAG Implementation Details

- **PDF Processing**: Uses PyMuPDF for efficient text extraction from PDF documents
- **Text Chunking**: Implements intelligent text splitting with 1000-character chunks and 200-character overlap
- **Embeddings**: Uses Ollama with `mxbai-embed-large` model for generating high-quality embeddings
- **Vector Search**: Employs cosine similarity for semantic document retrieval
- **Knowledge Base**: Currently contains Pakistan Universities curriculum outline (HEC document)
- **Caching**: Embeddings are cached and saved to disk for faster subsequent searches

## TODO - Future Enhancements

### ✅ Completed Features
- [x] **RAG System**: Document processing and semantic search implementation
- [x] **Multi-Tool Agent**: Weather, cryptocurrency, and knowledge base tools
- [x] **Agent Framework**: LangGraph-based agent with ReAct pattern
- [x] **Function Calling Agent**: Native Google Gemini function calling implementation

### 🚀 Advanced Features to Implement

#### Multi-Agent Systems
- [ ] **Agent Collaboration**: Multiple specialized agents working together
- [ ] **Agent Communication**: Inter-agent messaging and coordination protocols
- [ ] **Agent Orchestration**: Central coordinator managing multiple agents

#### Advanced RAG Enhancements
- [ ] **Hybrid Search**: Combine semantic and keyword-based search
- [ ] **Multi-Modal RAG**: Support for images, audio, and video documents
- [ ] **Dynamic Retrieval**: Adaptive retrieval based on query complexity

#### Agent Intelligence
- [ ] **Memory Systems**: Long-term and short-term memory for agents
- [ ] **Learning Agents**: Agents that improve from interactions
- [ ] **Planning Agents**: Advanced planning and goal decomposition
- [ ] **Reasoning Chains**: Multi-step logical reasoning capabilities
- [ ] **Self-Reflection**: Agents that can evaluate and improve their own performance

### 🎯 Learning Objectives
These enhancements will help explore:
- Advanced AI agent architectures
- Distributed systems and microservices
- Multi-agent coordination algorithms
- Advanced RAG techniques and evaluation
- Human-AI collaboration patterns
- Scalable AI system design
