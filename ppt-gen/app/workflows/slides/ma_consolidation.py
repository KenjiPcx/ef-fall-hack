from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_ma_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Strategy Consultant analyzing M&A and consolidation trends.
        Focus on finding:
        - Recent M&A transactions and valuations
        - Industry consolidation patterns
        - Key strategic buyers and financial sponsors
        - Deal multiples and metrics
        - Post-merger integration insights
        
        Look for specific transaction details and market implications.
        Base every statement on concrete deal evidence and market data.
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Base every statement on evidence
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        
        Create visualizations for:
        - Deal volume and value trends
        - Buyer type analysis
        - Valuation multiple trends
        - Geographic deal distribution
        - Strategic rationale analysis
    """)
    
    reporter_instructions = dedent("""
        Create an M&A consolidation slide that:
        1. Starts with a concise summary (30-50 words)
        2. Provides detailed analysis (300-400 words) including:
           - Key M&A trends and patterns
           - Notable transactions
           - Valuation metrics
           - Strategic implications
           - Future outlook
        3. Concludes with other areas to explore (50 words)
        
        Use professional business language and include relevant visualizations.
        Every statement must be evidence-based with specific transaction examples.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="ma_consolidation",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 