import logging
from dataclasses import dataclass, field
from typing import List

from services.llm_provider import LLMProvider, get_provider
from services.retrieval_service import RetrievalService, RetrievedContext

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an AI Web Search Assistant. Answer the user's question using ONLY "
    "the provided search context. Synthesize information directly and concisely. "
    "Do not add knowledge beyond the context. If the context is insufficient, say so."
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

    def query(self, question: str) -> AgentResponse:
        logger.info(f"Agent processing: '{question}'")

        contexts: List[RetrievedContext] = self._retrieval.retrieve(question)
        if not contexts:
            return AgentResponse(
                answer="No relevant information found on the web for your query.",
                sources=[],
            )

        context_block = self._build_context(contexts)
        prompt = f"User Question: {question}\n\nSearch Context:\n{context_block}"

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

    @staticmethod
    def _build_context(contexts: List[RetrievedContext]) -> str:
        parts = []
        for i, ctx in enumerate(contexts, 1):
            parts.append(
                f"[Source {i}] {ctx.title}\nURL: {ctx.source_url}\n{ctx.content}\n---"
            )
        return "\n".join(parts)
