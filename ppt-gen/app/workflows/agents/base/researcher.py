import os
from textwrap import dedent
from typing import List, Optional

from app.engine.index import IndexConfig, get_index
from app.engine.tools.retrieval_engine import get_retrieval_engine_tool
from app.workflows.single import FunctionCallingAgent
from llama_index.core.chat_engine.types import ChatMessage
from llama_index.core.tools import BaseTool, QueryEngineTool, ToolMetadata
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex


def _create_query_engine_tools(params=None, filters=None) -> Optional[list[type[BaseTool]]]:
    """
    Provide an agent worker that can be used to query the index.
    """
    # Add query tool if index exists
    index_config = IndexConfig(**(params or {}))
    index = get_index(index_config)
    if index is None:
        return None

    # Construct query engine tools
    retriever = get_retrieval_engine_tool(index)
    return [retriever]

def create_researcher(
    chat_history: List[ChatMessage], 
    additional_instructions: Optional[str] = None,
    **kwargs
):
    """
    Researcher is an agent that take responsibility for using tools to complete a given task.
    """
    tools = _create_query_engine_tools(**kwargs)

    if tools is None:
        raise ValueError("No tools found for researcher agent")

    base_prompt = dedent(
        """
        You are a researcher agent. You are responsible for retrieving information from a graphic rich data source.
        ## Instructions
        + First review the chat history to understand what information we already have
        + Focus on finding NEW relevant information that can tell a compelling story
        + Make 3 different queries to the retrieval engine to build a comprehensive view
        + Avoid repeating searches for information we already have
        + Prioritize finding information with supporting visuals
        + Look for concrete data points, statistics, and trends
        + For retrieved documents that are relevant, don't synthesize or summarize yet - collect the raw information
        + For retrieved documents that are not relevant, filter them out
        + Preserve all metadata, especially node_id, image_url and source fields
        
        Important: If the information you're looking for is already in the chat history,
        explicitly state that you're using existing information and don't perform redundant searches.
        """
    )

    if additional_instructions:
        base_prompt += f"\n\nAdditional Instructions:\n{additional_instructions}. When searching for information, tune your query to be relevant to your specialized role."

    return FunctionCallingAgent(
        name="Researcher",
        tools=tools,
        description="expert in retrieving any unknown content from the corpus",
        system_prompt=base_prompt,
        chat_history=chat_history.copy(),
    )
