"""LangGraph orchestration blueprint for the smart factory controller."""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode


class FactoryState(TypedDict):
    """Shared state that LangGraph nodes pass around."""

    messages: List[BaseMessage]
    context: Dict[str, Any]


async def llm_decider(state: FactoryState, llm: Runnable) -> FactoryState:
    """Entry point node responsible for calling the LLM for routing."""

    raise NotImplementedError("Bind an LLM runnable and author routing prompts here")


async def post_tool_report(state: FactoryState) -> FactoryState:
    """Summarize tool execution output for the frontend."""

    raise NotImplementedError("Implement reporting synthesis back to the UI")


def create_smart_factory_graph(llm: Runnable, tools: Sequence[Any]) -> Runnable:
    """Compile the LangGraph workflow used by the FastAPI endpoints."""

    graph = StateGraph(FactoryState)
    graph.add_node("llm_decider", lambda state: llm_decider(state, llm))
    graph.add_node("tool_executor", ToolNode(tools=tools))
    graph.add_node("post_tool_report", post_tool_report)

    graph.add_edge(START, "llm_decider")
    graph.add_edge("llm_decider", "tool_executor")
    graph.add_edge("tool_executor", "post_tool_report")
    graph.add_edge("post_tool_report", END)

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
