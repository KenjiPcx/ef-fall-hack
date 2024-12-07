from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_risks_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Strategy Consultant tasked with identifying key risks and challenges.
        Focus on finding:
        - Market and competitive risks
        - Regulatory and compliance risks
        - Operational and execution risks
        - Technology and disruption risks
        - Economic and macro risks
        
        Look for specific examples and quantifiable impacts.
        Base every statement on evidence from the knowledge base.
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Base every statement on evidence
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        
        Create visualizations for:
        - Risk impact assessment matrix
        - Risk probability analysis
        - Mitigation strategy framework
        - Historical risk events timeline
        - Risk correlation analysis
    """)
    
    reporter_instructions = dedent("""
        Create a risks slide that:
        1. Starts with a concise summary (30-50 words)
        2. Provides detailed analysis (300-400 words) including:
           - Key risk categories and their significance
           - Quantifiable impact assessments
           - Historical precedents
           - Mitigation strategies
           - Industry benchmarks
        3. Concludes with other areas to explore (50 words)
        
        Use professional business language and include relevant visualizations.
        Every statement must be evidence-based with specific examples.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="risks",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 