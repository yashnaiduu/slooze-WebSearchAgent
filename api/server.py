from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.search_agent import SearchAgent
from utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title="AI Web Search Agent",
    description="Search the web and get AI-synthesized answers with sources.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SearchAgent()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def search_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = agent.query(request.query)
    except Exception as exc:
        if "Ratelimit" in str(exc):
            raise HTTPException(
                status_code=503,
                detail="Search provider is rate-limited. Please wait a moment and try again.",
            )
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}")

    return QueryResponse(answer=result.answer, sources=result.sources)


if __name__ == "__main__":
    import uvicorn
    from config.settings import settings

    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
