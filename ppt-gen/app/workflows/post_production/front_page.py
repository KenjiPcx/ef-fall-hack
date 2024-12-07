from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from app.workflows.old_base_workflow import create_workflow

def create_front_page_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        Review the report to identify:
        - Main topic and scope
        - Key themes
        - Report coverage
        - Target audience
    """)
    
    analyst_instructions = dedent("""
        Analyze the report to:
        - Identify key sections
        - Create logical structure
        - Design clear hierarchy
        - Select key visuals if needed
    """)
    
    reporter_instructions = dedent("""
        Create a professional front page that includes:
        - Clear title reflecting content
        - Subtitle with key scope
        - Date and context
        - Professional formatting
        - Visual elements if appropriate
    """)
    
    return create_workflow(
        chat_history=chat_history,
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 