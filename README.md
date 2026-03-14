# AI Web Search Agent

An AI-powered web search tool that generates answers using live internet data.

---

## Overview

This system accepts natural language questions, searches the internet, and synthesizes answers. It extracts content from multiple webpages and uses an LLM to generate an accurate summary with citations.

---

## Features

* Web search functionality
* Page content extraction
* AI-synthesized responses
* Source link attribution
* Provider-agnostic LLM support

---

## Architecture

User Query
→ Search Tool
→ Retrieve Page Content
→ LLM Processing
→ Final Answer

---

## Project Structure

```text
agent/      # Main agent logic
tools/      # Search and webpage extraction
services/   # LLM and retrieval orchestration
api/        # FastAPI server endpoints
ui/         # Streamlit visual interface
config/     # Environment configuration
```

---

## Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Add environment variables
5. Run application

---

## Environment Variables

* `OPENAI_API_KEY`
* `LLM_PROVIDER`
* `LLM_MODEL`
* `SEARCH_PROVIDER`

---

## Running the Project

```bash
pip install -r requirements.txt
streamlit run ui/app.py
```

---

## Example Usage

**Question:**
"What are the latest developments in quantum computing?"

**Answer:**
Recent developments in quantum computing include advances in error correction and higher stable qubit counts.

**Sources:**
- https://example.com/quantum
- https://example.com/physics

---

## Design Decisions

* clean modular architecture
* provider-agnostic LLM layer
* decoupled search providers
