"""High-level service that wires FastAPI endpoints to LangGraph."""
from __future__ import annotations

import logging
from typing import Any, Dict

from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from ..config import settings
from ..schemas import QueryRequest
from .langgraph_factory import FactoryState, create_smart_factory_graph
from .tools import check_stock, machine_a, machine_b, machine_c, tool_check_schedule

logger = logging.getLogger(__name__)


class FactoryOrchestrator:
    """Facilitates conversations between the UI, tools, and LangGraph."""

    def __init__(self) -> None:
        self.tools = self._init_tools()
        self.llm = self._init_llm()
        self.graph = create_smart_factory_graph(self.llm, self.tools)

    def _init_llm(self) -> Runnable:
        """Return the ChatOpenAI client or a safe fallback when no key is configured."""

        if settings.openai_api_key:
            client_kwargs: Dict[str, Any] = {
                "model": settings.llm_model,
                "temperature": 0,
                "api_key": settings.openai_api_key,
            }
            if settings.openai_base_url:
                client_kwargs["base_url"] = settings.openai_base_url
            return ChatOpenAI(**client_kwargs)

        logger.warning(
            "OPENAI_API_KEY not set. Falling back to a mock LLM; /api/query responses "
            "will be placeholders until a real API key is provided."
        )
        return RunnableLambda(
            lambda messages: AIMessage(
                content="LLM unavailable: configure OPENAI_API_KEY to enable decisions."
            )
        )

    def _init_tools(self) -> list[Tool]:
        return [
            Tool.from_function(
                name="check_schedule",
                description="Inspect and reason about the production schedule JSON",
                func=tool_check_schedule,
            ),
            Tool.from_function(
                name="check_stock",
                description="Validate raw material inventory for a product",
                func=check_stock,
            ),
            Tool.from_function(
                name="machine_a",
                description="Reserve machine A for a production task",
                func=machine_a,
            ),
            Tool.from_function(
                name="machine_b",
                description="Reserve machine B for a production task",
                func=machine_b,
            ),
            Tool.from_function(
                name="machine_c",
                description="Reserve machine C for a production task",
                func=machine_c,
            ),
        ]

    async def run(self, payload: QueryRequest) -> Dict[str, Any]:
        state: FactoryState = {
            "messages": [],
            "context": {
                "query": payload.message,
                "metadata": payload.metadata or {},
            },
        }
        return await self.graph.ainvoke(state)


orchestrator = FactoryOrchestrator()
