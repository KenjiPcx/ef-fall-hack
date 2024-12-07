from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from app.workflows.old_base_workflow import create_workflow

def create_slide_workflow(
    chat_history: Optional[List[ChatMessage]] = None,
    slide_type: str = "",
    researcher_instructions: Optional[str] = None,
    analyst_instructions: Optional[str] = None,
    reporter_instructions: Optional[str] = None,
    **kwargs
):
    """Base function for creating slide-specific workflows"""
    return create_workflow(
        chat_history=chat_history,
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 