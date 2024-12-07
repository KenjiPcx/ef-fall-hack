from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from app.workflows.old_base_workflow import create_workflow

def create_executive_summary_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        Review all sections of the report and identify:
        - Key findings from each section
        - Critical market insights
        - Major trends and patterns
        - Strategic implications
    """)
    
    analyst_instructions = dedent("""
        Analyze the overall report to:
        - Identify top 3-5 key takeaways
        - Highlight critical market dynamics
        - Summarize growth potential
        - Note key risks and opportunities
    """)
    
    reporter_instructions = dedent("""
        Create an executive summary that:
        - Provides a clear overview in 1-2 pages
        - Highlights key findings and insights
        - Summarizes market opportunity
        - Includes critical data points
        - Maintains professional, concise language
    """)
    
    return create_workflow(
        chat_history=chat_history,
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 