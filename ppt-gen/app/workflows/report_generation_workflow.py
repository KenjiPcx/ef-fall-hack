from textwrap import dedent
from typing import AsyncGenerator, List, Optional

# Import slide workflows
from app.workflows.slides.market_size import create_market_size_workflow
from app.workflows.slides.growth_drivers import create_growth_drivers_workflow
from app.workflows.slides.risks import create_risks_workflow
from app.workflows.slides.ma_consolidation import create_ma_workflow
from app.workflows.slides.dynamics import create_dynamics_workflow
from app.workflows.slides.profiles import create_profiles_workflow

# Import post-production workflows
from app.workflows.post_production.executive_summary import create_executive_summary_workflow
from app.workflows.post_production.front_page import create_front_page_workflow

from app.workflows.single import AgentRunEvent, AgentRunResult
from llama_index.core.chat_engine.types import ChatMessage, ChatResponse
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

class StartSlideGenerationEvent(Event):
    input: str
    slide_type: str

class CombineReportEvent(Event):
    pass

class CreateExecutiveSummaryEvent(Event):
    input: str

class CreateFrontPageEvent(Event):
    input: str

class ReportGenerationWorkflow(Workflow):
    def __init__(
        self,
        timeout: int = 3600,
        chat_history: Optional[List[ChatMessage]] = None,
        initial_team_size: int = 6,  # Number of slide generators
        post_production_team_size: int = 2,  # Executive summary and front page
    ):
        super().__init__(timeout=timeout)
        self.chat_history = chat_history or []
        self.initial_team_size = initial_team_size
        self.post_production_team_size = post_production_team_size

    @step()
    async def start(self, ctx: Context, ev: StartEvent) -> StartSlideGenerationEvent:
        ctx.data["idea"] = ev.input
        
        # Decision-making process
        decision = await self._decide_workflow(ev.input, self.chat_history)
        
        if decision == "research":
            ctx.write_event_to_stream(
                AgentRunEvent(
                    name="Report Generation Workflow",
                    msg=f"Starting research on: {ev.input}",
                    workflow_name="Research Manager"
                )
            )
            
            # Start parallel slide generation
            slides = [
                "market_size",
                "growth_drivers",
                "risks",
                "ma_consolidation",
                "dynamics",
                "profiles"
            ]
            
            for slide in slides:
                ctx.send_event(StartSlideGenerationEvent(
                    input=ev.input,
                    slide_type=slide
                ))
            
            return None
        else:
            # Handle follow-up questions using existing information
            return StopEvent(result="Using existing information to answer follow-up")

    async def _decide_workflow(self, input: str, chat_history: List[ChatMessage]) -> str:
        prompt_template = PromptTemplate(
            dedent(
                """
                You are an expert in decision-making, helping to generate comprehensive market research reports.
                If this is a follow-up question that can be answered with existing information, respond with 'follow_up'.
                If this requires new research, respond with 'research'.

                Here is the chat history:
                {chat_history}

                The current user request is:
                {input}

                Decision (respond with either 'follow_up' or 'research'):
                """
            )
        )

        chat_history_str = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in chat_history]
        )
        prompt = prompt_template.format(chat_history=chat_history_str, input=input)

        output = await Settings.llm.acomplete(prompt)
        return output.text.strip().lower()

    @step()
    async def generate_market_size(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "market_size":
            return None
            
        workflow = create_market_size_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["market_size_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def generate_growth_drivers(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "growth_drivers":
            return None
            
        workflow = create_growth_drivers_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["growth_drivers_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def generate_risks(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "risks":
            return None
            
        workflow = create_risks_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["risks_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def generate_ma_consolidation(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "ma_consolidation":
            return None
            
        workflow = create_ma_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["ma_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def generate_dynamics(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "dynamics":
            return None
            
        workflow = create_dynamics_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["dynamics_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def generate_profiles(self, ctx: Context, ev: StartSlideGenerationEvent) -> CombineReportEvent:
        if ev.slide_type != "profiles":
            return None
            
        workflow = create_profiles_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["profiles_result"] = result
        ctx.data["slides_completed"] = ctx.data.get("slides_completed", 0) + 1
        return CombineReportEvent()

    @step()
    async def combine_report(self, ctx: Context, ev: CombineReportEvent) -> CreateExecutiveSummaryEvent | CreateFrontPageEvent:
        slides_completed = ctx.data.get("slides_completed", 0)
        if slides_completed < self.initial_team_size:
            ctx.write_event_to_stream(
                AgentRunEvent(
                    name="Report Generation Workflow",
                    msg=f"Collected {slides_completed} slides out of {self.initial_team_size}",
                    workflow_name="Research Manager"
                )
            )
            return None

        # Combine all slides
        combined_report = f"""
        Market Size: {ctx.data.get('market_size_result')}
        Growth Drivers: {ctx.data.get('growth_drivers_result')}
        Risks: {ctx.data.get('risks_result')}
        M&A: {ctx.data.get('ma_result')}
        Dynamics: {ctx.data.get('dynamics_result')}
        Profiles: {ctx.data.get('profiles_result')}
        """
        
        ctx.data["combined_report"] = combined_report
        ctx.send_event(CreateExecutiveSummaryEvent(input=combined_report))
        ctx.send_event(CreateFrontPageEvent(input=combined_report))
        return None

    @step()
    async def generate_executive_summary(self, ctx: Context, ev: CreateExecutiveSummaryEvent) -> StopEvent:
        # Create and run executive summary workflow
        workflow = create_executive_summary_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["executive_summary"] = result
        ctx.data["post_production_completed"] = ctx.data.get("post_production_completed", 0) + 1
        return None

    @step()
    async def generate_front_page(self, ctx: Context, ev: CreateFrontPageEvent) -> StopEvent:
        # Create and run front page workflow
        workflow = create_front_page_workflow(chat_history=self.chat_history)
        result = await self.run_sub_workflow(ctx, workflow, ev.input)
        
        ctx.data["front_page"] = result
        ctx.data["post_production_completed"] = ctx.data.get("post_production_completed", 0) + 1
        return None

    @step()
    async def finalize_report(self, ctx: Context, ev: Event) -> StopEvent:
        post_production_completed = ctx.data.get("post_production_completed", 0)
        if post_production_completed < self.post_production_team_size:
            return None

        final_report = f"""
        {ctx.data.get('front_page')}
        
        Executive Summary:
        {ctx.data.get('executive_summary')}
        
        {ctx.data.get('combined_report')}
        """
        
        return StopEvent(result=final_report)

    async def run_sub_workflow(
        self,
        ctx: Context,
        workflow: Workflow,
        input: str,
        workflow_name: str = ""
    ) -> AgentRunResult | AsyncGenerator:
        try:
            handler = workflow.run(input=input)
            async for event in handler.stream_events():
                if type(event) is not StopEvent:
                    if isinstance(event, AgentRunEvent):
                        event.workflow_name = workflow_name
                    ctx.write_event_to_stream(event)
            return await handler
        except Exception as e:
            error_message = f"Error in {workflow_name}: {str(e)}"
            ctx.write_event_to_stream(
                AgentRunEvent(
                    name="Report Generation Workflow",
                    msg=error_message,
                    workflow_name=workflow_name
                )
            )
            return AgentRunResult(
                response=ChatResponse(
                    message=ChatMessage(
                        content=f"Failed to complete {workflow_name} due to an error: {str(e)}"
                    )
                ),
                sources=[]
            )

def create_report_generation_workflow(
    chat_history: Optional[List[ChatMessage]] = None,
    **kwargs
) -> ReportGenerationWorkflow:
    workflow = ReportGenerationWorkflow(
        timeout=3600,
        chat_history=chat_history,
        initial_team_size=6,
        post_production_team_size=2
    )
    return workflow 