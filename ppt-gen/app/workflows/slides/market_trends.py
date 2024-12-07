from textwrap import dedent
from typing import Optional, List
from llama_index.core.chat_engine.types import ChatMessage
from .base_slide import create_slide_workflow

def create_market_trends_workflow(chat_history: Optional[List[ChatMessage]] = None, **kwargs):
    researcher_instructions = dedent("""
        You are a Senior Strategy Consultant tasked with answering queries about a knowledge base. Your responses should be comprehensive, insightful, and directly aligned with the uploaded content.
        
        Your audience is a Private Equity firm conducting a due diligence report.
        
        Follow these steps:
        1. Carefully analyze the query and uploaded content
        2. Generate a detailed response (300-500 words)
        3. Ensure no relevant insight is omitted
        4. Adhere strictly to the knowledge base content
        5. Structure your response clearly
        
        Do not add, interpret, or infer beyond the explicit information provided.
        If information cannot be found, state: "I could not find an accurate answer in my knowledge base."
    """)
    
    analyst_instructions = dedent("""
        Analyze the research results to create:
        1. Summary (30-50 words)
        2. Detailed Analysis (300 words)
        3. Other areas to explore (50 words)
        
        Use charts and visualizations to support key trends and patterns.
        Focus on data-driven insights and clear visual representation of trends.
    """)
    
    reporter_instructions = dedent("""
        Create a market trends slide following these principles:
        1. Detail: Dense, detail-rich content with precise information
        2. Evidence-Based: Include specific numbers, quotes, facts
        3. Avoid Fluff: Eliminate unnecessary words
        4. Professional Language: Clear, neutral business language
        5. Structure: Follow the format:
           - Summary (30-50 words)
           - Detailed Analysis (300-400 words)
           - Other Areas to Explore (50 words)
        
        Include relevant visualizations from the analysis.
    """)
    
    return create_slide_workflow(
        chat_history=chat_history,
        slide_type="market_trends",
        researcher_instructions=researcher_instructions,
        analyst_instructions=analyst_instructions,
        reporter_instructions=reporter_instructions,
        **kwargs
    ) 