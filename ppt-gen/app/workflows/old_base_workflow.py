from textwrap import dedent
from typing import AsyncGenerator, List, Optional

from app.workflows.agents.base.analyst import create_analyst
from app.workflows.agents.base.reporter import create_reporter
from app.workflows.agents.base.researcher import create_researcher
from app.workflows.single import AgentRunEvent, AgentRunResult, FunctionCallingAgent
from llama_index.core.chat_engine.types import ChatMessage
from llama_index.core.prompts import PromptTemplate
from llama_index.core.settings import Settings
from llama_index.core.workflow import (
    Context,
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

import logging
logger = logging.getLogger(__name__)

def create_workflow(
    chat_history: Optional[List[ChatMessage]] = None,
    researcher_instructions: Optional[str] = None,
    analyst_instructions: Optional[str] = None,
    reporter_instructions: Optional[str] = None,
    **kwargs
):
    researcher = create_researcher(
        chat_history=chat_history,
        additional_instructions=researcher_instructions,
        **kwargs,
    )
    analyst = create_analyst(
        chat_history=chat_history,
        additional_instructions=analyst_instructions
    )
    reporter = create_reporter(
        chat_history=chat_history,
        additional_instructions=reporter_instructions
    )
    workflow = BaseWorkflow(timeout=360, chat_history=chat_history)

    workflow.add_workflows(
        researcher=researcher,
        analyst=analyst,
        reporter=reporter,
    )
    return workflow


class ResearchEvent(Event):
    input: str


class AnalyzeEvent(Event):
    input: str


class ReportEvent(Event):
    input: str


class BaseWorkflow(Workflow):
    def __init__(
        self, 
        timeout: int = 360, 
        chat_history: Optional[List[ChatMessage]] = None
    ):
        super().__init__(timeout=timeout)
        self.chat_history = chat_history or []

    @step()
    async def start(self, ctx: Context, ev: StartEvent) -> ResearchEvent | ReportEvent:
        # set streaming
        ctx.data["streaming"] = getattr(ev, "streaming", False)
        # start the workflow with researching about a topic
        ctx.data["task"] = ev.input
        ctx.data["user_input"] = ev.input

        return ResearchEvent(input=f"Research for this task: {ev.input}")
            
    @step()
    async def research(
        self, ctx: Context, ev: ResearchEvent, researcher: FunctionCallingAgent
    ) -> AnalyzeEvent:
        result: AgentRunResult = await self.run_agent(ctx, researcher, ev.input)
        logger.info(f"Research result: {result}")
        content = result.response.message.content
        ctx.write_event_to_stream(
            AgentRunEvent(
                name=researcher.name,
                msg=f"Completed research: {content}",
            )       
        )
        ctx.data["research_results"] = content
        return AnalyzeEvent(
            input=dedent(
                f"""
                You have been given search results from a private knowledge base consisting a diverse set of visual rich content, your role is to come up with new insights from the search results and use the interpreter tool to create visualizations, charts, relationships and graphs.
                
                Here are the search results:
                {content}
                """
            )
        )

    @step()
    async def analyze(
        self, ctx: Context, ev: AnalyzeEvent, analyst: FunctionCallingAgent
    ) -> ReportEvent | StopEvent:
        result: AgentRunResult = await self.run_agent(ctx, analyst, ev.input)
        content = result.response.message.content
        ctx.write_event_to_stream(
            AgentRunEvent(
                name=analyst.name,
                msg=f"Completed analysis: {content}",
            )       
        )
        return ReportEvent(
            input=dedent(
                f"""
                You have been given both search results from a private knowledge base consisting a diverse set of visual rich content, and further insights generated from an analyst on the data, now present it in a report.
                
                Here are the initial search results:
                {ctx.data["research_results"]}
                
                Here are the further insights:
                {content}
                
                Now create a report for the user's request: {ctx.data["task"]}
                """
            )
        )
        
    @step()
    async def report(
        self, ctx: Context, ev: ReportEvent, reporter: FunctionCallingAgent
    ) -> StopEvent:
        try:
            result: AgentRunResult = await self.run_agent(
                ctx, reporter, ev.input, streaming=ctx.data["streaming"]
            )
            
            return StopEvent(result=result)
        except Exception as e:
            ctx.write_event_to_stream(
                AgentRunEvent(
                    name=reporter.name,
                    msg=f"Error creating a report: {e}",
                )
            )
            return StopEvent(result=None)

    async def run_agent(
        self,
        ctx: Context,
        agent: FunctionCallingAgent,
        input: str,
        streaming: bool = False,
    ) -> AgentRunResult | AsyncGenerator:
        handler = agent.run(input=input, streaming=streaming)
        # bubble all events while running the executor to the planner
        async for event in handler.stream_events():
            # Don't write the StopEvent from sub task to the stream
            if type(event) is not StopEvent:
                ctx.write_event_to_stream(event)
        return await handler
