from textwrap import dedent
from typing import List, Optional, Tuple, Dict

from app.engine.tools import ToolFactory
from app.engine.tools.interpreter import E2BCodeInterpreter
from app.workflows.single import FunctionCallingAgent
from llama_index.core.chat_engine.types import ChatMessage
from llama_index.core.tools import FunctionTool


def _get_analyst_params() -> Tuple[List[type[FunctionTool]], str, str]:
    tools = []
    base_prompt = dedent(
        """
        You are an expert in analyzing financial data.
        You are given a task and a set of financial data to analyze. Your task is to analyze the financial data and return a report.
        Your response should include a detailed analysis of the financial data, including any trends, patterns, or insights that you find.
        Construct the analysis in a textual format like tables would be great!
        Don't need to synthesize the data, just analyze and provide your findings.
        Always use the provided information, don't make up any information yourself.
        """
    )
    description = "Expert in analyzing financial data"
    # Check if the interpreter tool is configured
    # tools = [FunctionTool.from_defaults(E2BCodeInterpreter().interpret)]
    configured_tools: Dict[str, FunctionTool] = ToolFactory.from_env(map_result=True)  # type: ignore
    print(f"Configured tools: {configured_tools}")
    code_interpreter_tool = configured_tools.get("interpret")
    if code_interpreter_tool:
        tools.append(code_interpreter_tool)
        base_prompt += dedent("""
            You can use the interpreter tool to execute code, create charts and graphs.
            It's very useful to create and include visualizations to the report (make sure you include the right code and data for the visualization).
            Never include any code into the report, just the visualization.
        """)
        description += ", able to visualize the financial data using code interpreter tool."
    return tools, base_prompt, description


def create_analyst(
    chat_history: List[ChatMessage],
    additional_instructions: Optional[str] = None,
    **kwargs
):
    tools, base_prompt, description = _get_analyst_params()

    if additional_instructions:
        base_prompt += f"\n\nAdditional Instructions:\n{additional_instructions}"

    return FunctionCallingAgent(
        name="Analyst",
        tools=tools,
        description=description,
        system_prompt=base_prompt,
        chat_history=chat_history.copy(),
    )
