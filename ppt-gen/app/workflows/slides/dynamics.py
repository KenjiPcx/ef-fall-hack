from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_dynamics_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Strategy Consultant analyzing market dynamics and competitive landscape.
        Focus on finding:
        - Competitive intensity and market structure
        - Entry barriers and switching costs
        - Supplier/buyer power dynamics
        - Substitution threats
        - Industry value chain analysis
        
        Look for specific examples and market evidence.
        Base every statement on concrete competitive dynamics data.
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Base every statement on evidence
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        
        Create visualizations for:
        - Competitive positioning matrix
        - Market share evolution
        - Value chain economics
        - Porter's Five Forces analysis
        - Industry profit pool distribution
    """)
    
    reporter_instructions = dedent("""
        Create a market dynamics slide that:
        1. Starts with a concise summary (30-50 words)
        2. Provides detailed analysis (300-400 words) including:
           - Competitive landscape overview
           - Key success factors
           - Value chain dynamics
           - Barriers to entry
           - Industry profitability drivers
        3. Concludes with other areas to explore (50 words)
        
        Use professional business language and include relevant visualizations.
        Every statement must be evidence-based with specific competitive examples.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="dynamics",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 