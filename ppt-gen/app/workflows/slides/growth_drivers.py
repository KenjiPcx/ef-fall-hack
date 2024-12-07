from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_growth_drivers_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        Focus on finding:
        - Key growth drivers in the market
        - Industry trends driving growth
        - Technology innovations
        - Regulatory impacts
        - Consumer behavior changes
        Look for specific examples and data points.
    """)
    
    analyst_instructions = dedent("""
        Create visualizations and analysis for:
        - Impact of each growth driver
        - Trend analysis
        - Correlation between drivers
        - Future impact projections
        Use charts and graphs to show relationships.
    """)
    
    reporter_instructions = dedent("""
        Create a growth drivers slide that includes:
        - Key growth drivers overview
        - Impact analysis
        - Supporting trends
        - Future implications
        Include relevant charts and visuals.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="growth_drivers",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 