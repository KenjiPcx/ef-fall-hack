from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_market_size_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Strategy Consultant tasked with finding market sizing information.
        Focus on finding:
        - Total market size (TAM, SAM, SOM)
        - Historical market data and growth rates
        - Future market projections and forecasts
        - Key market segments and their sizes
        - Regional market breakdowns
        
        Look for concrete numbers and statistics with sources.
        Base every statement on evidence, such as specific numbers, quotes, or facts.
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Base every statement on evidence
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        
        Create visualizations for:
        - Market size evolution over time
        - Growth rate trends
        - Market segmentation
        - Geographic distribution
        - Future projections
    """)
    
    reporter_instructions = dedent("""
        Create a market size slide that:
        1. Starts with a concise summary (30-50 words)
        2. Provides detailed analysis (300-400 words) including:
           - Clear statement of current market size
           - Historical growth trajectory
           - Future growth projections
           - Key market segments
           - Geographic breakdown
        3. Concludes with other areas to explore (50 words)
        
        Use professional business language and include relevant visualizations.
        Every statement must be evidence-based with specific numbers.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="market_size",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 