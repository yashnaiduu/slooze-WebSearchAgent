# 🌐 AI Web Search Agent

A production-grade AI agent that searches the web, synthesizes information, and provides fully cited answers — powered by **Serper.dev** (Google Search) and **Groq LLMs**.

![Web Search Agent Demo](assets/demo.png)

## 🏗 Architecture

- **Frontend:** Streamlit chat interface (`ui/app.py`)
- **Backend:** FastAPI inference engine (`api/server.py`)
- **Search:** Serper.dev (primary) / DuckDuckGo (fallback) (`tools/`)
- **LLM:** Groq / OpenAI-compatible APIs (`services/`)

## ⚙️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY and SERPER_API_KEY
```

## 🚀 Run

```bash
python run.py
```

- Backend API: `http://localhost:8000`
- Streamlit UI: `http://localhost:8501`

Press `Ctrl+C` to shut down both services.

## Environment Variables

| Variable | Description |
|---|---|
| `LLM_PROVIDER` | `openai_compatible` (default for Groq) |
| `LLM_MODEL` | e.g. `llama-3.3-70b-versatile` |
| `GROQ_API_KEY` | Your Groq API key |
| `SERPER_API_KEY` | Your Serper.dev API key |
| `SEARCH_PROVIDER` | `serper` or `duckduckgo` |

## Design Decisions

- **Modular** — search, extraction, and generation are fully decoupled
- **Provider-agnostic** — swap LLMs with a single env variable
- **Reliable search** — Serper.dev for Google results, DuckDuckGo as keyless fallback
- **Lightweight** — no vector DB or persistent state required
