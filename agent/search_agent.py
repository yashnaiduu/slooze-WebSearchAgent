import logging
from dataclasses import dataclass, field
from typing import List, Optional

from services.llm_provider import LLMProvider, get_provider
from services.retrieval_service import RetrievalService, RetrievedContext

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an AI Web Search Assistant. Answer the user's question using ONLY "
    "the provided search context. Synthesize information directly and concisely. "
    "Do not add knowledge beyond the context. If the context is insufficient, say so."
)

REWRITE_PROMPT = (
    "Given the conversation history below, rewrite the latest user message into a "
    "standalone search query that captures the full intent. If it is already standalone, "
    "return it unchanged. Output ONLY the rewritten query, nothing else."
)


@dataclass
class AgentResponse:
    answer: str
    sources: List[str] = field(default_factory=list)


class SearchAgent:
    def __init__(
        self,
        llm: LLMProvider | None = None,
        retrieval: RetrievalService | None = None,
    ):
        self._llm = llm or get_provider()
        self._retrieval = retrieval or RetrievalService()

    def query(self, question: str, history: Optional[List[dict]] = None) -> AgentResponse:
        search_query = self._rewrite_query(question, history) if history else question
        logger.info(f"Agent processing: '{question}' -> search: '{search_query}'")

        contexts: List[RetrievedContext] = self._retrieval.retrieve(search_query)
        if not contexts:
            return AgentResponse(
                answer="No relevant information found on the web for your query.",
                sources=[],
            )

        context_block = self._build_context(contexts)

        # Build LLM prompt with conversation history for coherent answers
        history_block = ""
        if history:
            recent = history[-6:]  # last 3 exchanges
            lines = [f"{m['role'].capitalize()}: {m['content'][:200]}" for m in recent]
            history_block = "Conversation History:\n" + "\n".join(lines) + "\n\n"

        prompt = f"{history_block}User Question: {question}\n\nSearch Context:\n{context_block}"

        try:
            answer = self._llm.generate(prompt, system_prompt=SYSTEM_PROMPT)
        except Exception as exc:
            logger.error(f"LLM generation failed: {exc}")
            return AgentResponse(
                answer=f"Error generating answer: {exc}",
                sources=[ctx.source_url for ctx in contexts],
            )

        return AgentResponse(
            answer=answer,
            sources=[ctx.source_url for ctx in contexts],
        )

    def _rewrite_query(self, question: str, history: List[dict]) -> str:
        recent = history[-6:]
        lines = [f"{m['role'].capitalize()}: {m['content'][:200]}" for m in recent]
        conversation = "\n".join(lines)
        prompt = f"Conversation:\n{conversation}\n\nLatest message: {question}"

        try:
            rewritten = self._llm.generate(prompt, system_prompt=REWRITE_PROMPT)
            rewritten = rewritten.strip().strip('"').strip("'")
            if rewritten:
                return rewritten
        except Exception as exc:
            logger.warning(f"Query rewrite failed, using original: {exc}")

        return question

    @staticmethod
    def _build_context(contexts: List[RetrievedContext]) -> str:
        parts = []
        for i, ctx in enumerate(contexts, 1):
            parts.append(
                f"[Source {i}] {ctx.title}\nURL: {ctx.source_url}\n{ctx.content}\n---"
            )
        return "\n".join(parts)
