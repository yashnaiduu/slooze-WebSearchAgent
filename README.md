# AI Web Search Agent

An AI-powered agent that searches the web and generates grounded answers using live internet data.

## Architecture

```
User Query
  → Search Tool (DuckDuckGo / Tavily / SerpAPI)
  → Retrieve Top Results
  → Extract Page Content
  → LLM Reasoning (OpenAI / Anthropic / Ollama)
  → Answer + Sources
```

```
ai-web-search-agent/
├── agent/
│   └── search_agent.py        # Main agent pipeline
├── tools/
│   ├── search_tool.py         # Search provider abstraction
│   └── webpage_loader.py      # Page content extraction
├── services/
│   ├── llm_provider.py        # Multi-provider LLM interface
│   └── retrieval_service.py   # Search + extraction orchestration
├── api/
│   └── server.py              # FastAPI server
├── config/
│   └── settings.py            # Environment-based configuration
├── utils/
│   └── logging.py             # Logging setup
└── tests/
    └── test_search_agent.py
```

## Supported LLM Providers

| Provider | `LLM_PROVIDER` | Required Keys |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Ollama | `ollama` | `OLLAMA_BASE_URL` |
| OpenAI-Compatible | `openai_compatible` | `OPENAI_API_KEY`, `OPENAI_BASE_URL` |

## Setup

```bash
# Clone
git clone https://github.com/<your-username>/ai-web-search-agent.git
cd ai-web-search-agent

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your provider keys
```

## Usage

### API Server

```bash
python -m api.server
# Server starts at http://localhost:8000
```

### API Endpoints

**Search Query**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest developments in quantum computing?"}'
```

Response:
```json
{
  "answer": "Recent developments in quantum computing include...",
  "sources": [
    "https://example.com/quantum-2024",
    "https://example.com/quantum-breakthroughs"
  ]
}
```

**Health Check**
```bash
curl http://localhost:8000/health
```

### Python SDK

```python
from agent.search_agent import SearchAgent

agent = SearchAgent()
print(result.answer)
for url in result.sources:
    print(f"  - {url}")
```

### Streamlit UI

```bash
# Ensure requirements are installed
pip install -r requirements.txt

# Run the UI
streamlit run ui/app.py
```

## Example Queries

- "What are the latest AI regulations in the EU?"
- "Compare Python 3.12 vs 3.11 performance improvements"
- "Current weather in San Francisco"
- "Latest SpaceX launch details"

## Configuration

All settings are managed via environment variables or `.env` file. See `.env.example` for the full list.

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `openai` | LLM backend |
| `LLM_MODEL` | `gpt-4o-mini` | Model name |
| `SEARCH_PROVIDER` | `duckduckgo` | Search backend |
| `MAX_SEARCH_RESULTS` | `5` | Results per query |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Tests

```bash
python -m pytest tests/ -v
```

## License

MIT
