from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_profiles_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Strategy Consultant analyzing key market players and competitors.
        Focus on finding:
        - Company market positions and strategies
        - Financial performance metrics
        - Product/service portfolios
        - Operational capabilities
        - Growth initiatives and investments
        
        Look for specific company data and competitive intelligence.
        Base every statement on verifiable company information.
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Base every statement on evidence
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        
        Create visualizations for:
        - Competitive benchmarking matrix
        - Financial performance comparison
        - Market position mapping
        - Capability assessment
        - Strategic focus areas
    """)
    
    reporter_instructions = dedent("""
        Create a competitor profiles slide that:
        1. Starts with a concise summary (30-50 words)
        2. Provides detailed analysis (300-400 words) including:
           - Key player overview
           - Performance metrics
           - Strategic positioning
           - Competitive advantages
           - Future strategies
        3. Concludes with other areas to explore (50 words)
        
        Use professional business language and include relevant visualizations.
        Every statement must be evidence-based with specific company examples.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="profiles",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 