import os
from typing import Optional
from llama_index.core.tools.retriever_tool import RetrieverTool
from app.engine.postprocessors import NodeCitationProcessor, NodeMetadataRemover
from llama_index.core.indices import VectorStoreIndex

def get_retrieval_engine_tool(
    index: VectorStoreIndex,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> RetrieverTool:
    """
    Get a retrieval engine tool for the given index.

    Args:
        index: The index to create a retrieval engine for.
        name (optional): The name of the tool.
        description (optional): The description of the tool.
    """
    if name is None:
        name = "retrieve_index"
    if description is None:
        description = (
            "Use this tool to retrieve information about the text corpus from an index. "
            "Include as much context in the search query as possible, you need to communicate specifically what kind of information you are looking for."
        )
    top_k = int(os.getenv("TOP_K", 5))
    retrieval_engine = index.as_retriever(
        **({"similarity_top_k": top_k} if top_k != 0 else {})
    )
    
    return RetrieverTool.from_defaults(
        retriever=retrieval_engine,
        name=name,
        description=description,
    )