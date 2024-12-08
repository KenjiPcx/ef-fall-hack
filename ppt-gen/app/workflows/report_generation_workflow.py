from textwrap import dedent
from typing import AsyncGenerator, List, Optional

# Import slide workflows
from app.workflows.agents.base.reporter import create_reporter
from app.workflows.old_base_workflow import AnalyzeEvent, ReportEvent
from app.workflows.slides.market_size import create_market_size_workflow
from app.workflows.slides.growth_drivers import create_growth_drivers_workflow
from app.workflows.slides.risks import create_risks_workflow
from app.workflows.slides.ma_consolidation import create_ma_workflow
from app.workflows.slides.dynamics import create_dynamics_workflow
from app.workflows.slides.profiles import create_profiles_workflow

# Import post-production workflows
# from app.workflows.post_production.executive_summary import create_executive_summary_workflow
# from app.workflows.post_production.front_page import create_front_page_workflow

from app.workflows.single import AgentRunEvent, AgentRunResult, FunctionCallingAgent
from llama_index.core.llms import ChatMessage, ChatResponse
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
    slide_type: str
    input: str
    
class CombineReportEvent(Event):
    pass

class GenerateQueriesEvent(Event):
    input: str

class InitialResearchEvent(Event):
    queries: List[str]

class ReportGenerationWorkflow(Workflow):
    def __init__(
        self,
        timeout: int = 3600,
        chat_history: Optional[List[ChatMessage]] = None,
        initial_team_size: int = 6,
        post_production_team_size: int = 2,
    ):
        super().__init__(timeout=timeout)
        self.chat_history = chat_history or []
        self.initial_team_size = initial_team_size
        self.post_production_team_size = post_production_team_size

    @step()
    async def start(self, ctx: Context, ev: StartEvent) -> GenerateQueriesEvent | StartSlideGenerationEvent | StopEvent:
        ctx.data["idea"] = ev.input
        ctx.data["task"] = ev.input
        ctx.data["user_input"] = ev.input
        
        ctx.write_event_to_stream(
            AgentRunEvent(
                name="Report Generation Workflow",
                msg=f"Starting workflow for: {ev.input}",
                workflow_name="Research Manager"
            )
        )
        
        # Move to decision making
        return await self._decide_workflow(ev.input, self.chat_history)

    async def _decide_workflow(self, input: str, chat_history: List[ChatMessage]) -> GenerateQueriesEvent | StopEvent:
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
        decision = output.text.strip().lower()

        if decision == "research":
            return GenerateQueriesEvent(input=input)
        else:
            return StopEvent(result="Using existing information to answer follow-up")
        
    # @step()
    # async def analyze(
    #     self, ctx: Context, ev: AnalyzeEvent, analyst: FunctionCallingAgent
    # ) -> ReportEvent:
    #     result: AgentRunResult = await self.run_agent(ctx, analyst, ev.input)
    #     content = result.response.message.content
    #     ctx.write_event_to_stream(
    #         AgentRunEvent(
    #             name=analyst.name,
    #             msg=f"Completed analysis: {content}",
    #         )       
    #     )
    #     return ReportEvent(
    #         input=dedent(
    #             f"""
    #             You have been asked a follow up question on your previous analysis.
                
    #             Answer the user's question using the information already provided in the analysis.
    #             """
    #         )
    #     )
        
    @step()
    async def report(
        self, ctx: Context, ev: ReportEvent
    ) -> StopEvent:
        try:
            reporter = create_reporter(chat_history=self.chat_history)
            result: AgentRunResult = await self.run_agent(
                ctx, reporter, ev.input, streaming=False
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
    
    @step()
    async def generate_queries(self, ctx: Context, ev: GenerateQueriesEvent) -> InitialResearchEvent:
        prompt = PromptTemplate(
            dedent("""
                You are a research planning expert. Given a research topic, generate 3-5 broad, comprehensive queries 
                that will help gather initial information for a market research report covering:
                - Market size and forecasts
                - Growth drivers and trends
                - Risks and challenges
                - M&A and consolidation
                - Competitive dynamics
                - Key player profiles

                Research Topic: {input}

                Generate queries that:
                1. Are broad enough to capture comprehensive information
                2. Cover different aspects of the topic
                3. Will provide foundational knowledge for detailed analysis

                Format your response as a list of queries only, one per line.
            """)
        )

        formatted_prompt = prompt.format(input=ev.input)
        result = await Settings.llm.acomplete(formatted_prompt)
        queries = [q.strip() for q in result.text.split('\n') if q.strip()]
        
        ctx.write_event_to_stream(
            AgentRunEvent(
                name="Report Generation Workflow",
                msg=f"Generated initial research queries:\n{queries}",
                workflow_name="Research Manager"
            )
        )
        
        return InitialResearchEvent(queries=queries)

    @step()
    async def conduct_initial_research(self, ctx: Context, ev: InitialResearchEvent) -> StartSlideGenerationEvent:
        from app.engine.index import get_index
        from app.engine.tools.retrieval_engine import get_retrieval_engine_tool
        
        # Get the retrieval tool directly
        index = get_index()
        if index is None:
            raise ValueError("No index found for initial research")
            
        retriever = index.as_retriever(top_k=10)
        
        # Run each query and collect results
        all_results = []
        for query in ev.queries:
            ctx.write_event_to_stream(
                AgentRunEvent(
                    name="Report Generation Workflow",
                    msg=f"Running initial research query: {query}",
                    workflow_name="Initial Research"
                )
            )
            
            result = await retriever.aretrieve(query)
            all_results.append(result)
        
        # Add results to chat history
        combined_results = "\n\n".join([str(r) for r in all_results])
        ctx.data["initial_research_results"] = combined_results
        self.chat_history.append(
            ChatMessage(
                role="assistant",
                content=f"Initial Research Results:\n{combined_results}"
            )
        )
        
        ctx.write_event_to_stream(
            AgentRunEvent(
                name="Report Generation Workflow",
                msg="Completed initial research, starting slide generation",
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
                slide_type=slide,
                input=ctx.data["task"]
            ))
        
        return None

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
    async def combine_report(self, ctx: Context, ev: CombineReportEvent) -> ReportEvent:
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
        ## Market Size: 
        {ctx.data.get('market_size_result')}
        
        ---
        
        ## Growth Drivers: 
        {ctx.data.get('growth_drivers_result')}
        
        ---
        
        ## Risks: 
        {ctx.data.get('risks_result')}
        
        ---
        
        ## M&A: 
        {ctx.data.get('ma_result')}
        
        ---
        
        ## Dynamics: 
        {ctx.data.get('dynamics_result')}
        
        ---
        
        ## Profiles: 
        {ctx.data.get('profiles_result')}
        """
        print(f"Combined report:\n{combined_report}")
        ctx.data["combined_report"] = combined_report
        res_agent = FunctionCallingAgent(
            name="Executive Summarizer",
            tools=[],
            description="Expert in summarizing a report",
            system_prompt=dedent("""
                You are an expert in displaying reports.
                Your team will have created individual content for different slides in a report.
                Render them together in markdown information.
                Each slide should have their own pictures, just make it look nice.
            """),
        )
        
        prompt = f"Your team has created individual content for different slides in a report. Render them together with proper formatting like with markdown headers, bold, italic etc. Here is the combined report:\n{combined_report}\nEach slide should have their own pictures, just make it look nice. You can find some initial research results here:\n{ctx.data.get('initial_research_results')}, use them to replace any missing images."
        res = await self.run_agent(ctx, res_agent, prompt, True)
        
        return StopEvent(result=res)


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


def create_report_generation_workflow(
    chat_history: Optional[List[ChatMessage]] = None,
    **kwargs
) -> ReportGenerationWorkflow:
    # Create base agents for follow-up questions
    # analyst = create_analyst(chat_history=chat_history)
    # reporter = create_reporter(chat_history=chat_history)
    
    workflow = ReportGenerationWorkflow(
        timeout=3600,
        chat_history=chat_history,
        initial_team_size=6,
        post_production_team_size=2
    )
    
    # # Add the analyst and reporter for follow-up questions
    # workflow.add_workflows(
    #     analyst=analyst,
    #     reporter=reporter,
    # )
    
    return workflow 