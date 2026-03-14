from unittest.mock import MagicMock, patch

from agent.search_agent import AgentResponse, SearchAgent
from services.retrieval_service import RetrievedContext


def _mock_contexts():
    return [
        RetrievedContext(
            content="Python 3.12 was released in October 2023.",
            source_url="https://python.org/downloads",
            title="Python Releases",
        ),
        RetrievedContext(
            content="Python 3.12 introduces new typing features and performance improvements.",
            source_url="https://docs.python.org/3.12/whatsnew",
            title="What's New in Python 3.12",
        ),
    ]


class TestSearchAgent:
    def test_query_returns_structured_response(self):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Python 3.12 was released in October 2023 with typing and perf improvements."

        mock_retrieval = MagicMock()
        mock_retrieval.retrieve.return_value = _mock_contexts()

        agent = SearchAgent(llm=mock_llm, retrieval=mock_retrieval)
        result = agent.query("What is new in Python 3.12?")

        assert isinstance(result, AgentResponse)
        assert "Python 3.12" in result.answer
        assert len(result.sources) == 2
        mock_llm.generate.assert_called_once()

    def test_query_no_results(self):
        mock_llm = MagicMock()
        mock_retrieval = MagicMock()
        mock_retrieval.retrieve.return_value = []

        agent = SearchAgent(llm=mock_llm, retrieval=mock_retrieval)
        result = agent.query("nonexistent topic xyz")

        assert "No relevant information" in result.answer
        assert result.sources == []
        mock_llm.generate.assert_not_called()

    def test_query_llm_failure_returns_error(self):
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = RuntimeError("API error")

        mock_retrieval = MagicMock()
        mock_retrieval.retrieve.return_value = _mock_contexts()

        agent = SearchAgent(llm=mock_llm, retrieval=mock_retrieval)
        result = agent.query("test query")

        assert "Error generating answer" in result.answer
        assert len(result.sources) == 2
