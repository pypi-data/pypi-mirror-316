from contextlib import asynccontextmanager
import logging
import os
from fastapi import BackgroundTasks, FastAPI, Response
import uvicorn
from gru.agents.checkpoint.agent_prompts import AgentPromptsRepository, PromptStatus
from gru.agents.framework_wrappers import AgentWorkflow
from gru.agents.schemas import AgentInvokeRequest, AgentInvokeResponse
from gru.agents.schemas.schemas import PromptResultRequest, PromptResultResponse, TaskCompleteRequest

logger = logging.getLogger(__name__)

AGENT_NAME = os.getenv("AGENT_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):

    workflow: AgentWorkflow = app.state.workflow
    await workflow.setup()

    prompts_repo = AgentPromptsRepository()
    await prompts_repo.setup()

    app.state.prompts_repo = prompts_repo
    yield
        
api = FastAPI(lifespan=lifespan)

async def invoke_workflow(request: AgentInvokeRequest):

    prompts_repo: AgentPromptsRepository = api.state.prompts_repo
    await prompts_repo.update_result(AGENT_NAME, request.prompt_id, PromptStatus.PROCESSING)
    
    workflow: AgentWorkflow = api.state.workflow
    result, processing_complete = await workflow.invoke(request)
    if processing_complete:
        await prompts_repo.update_result(AGENT_NAME, request.prompt_id, PromptStatus.SUCCESS, result)


async def resume_workflow(request: TaskCompleteRequest):
    workflow: AgentWorkflow = api.state.workflow
    result, processing_complete = await workflow.resume(request)
    if processing_complete:
        prompts_repo: AgentPromptsRepository = api.state.prompts_repo
        await prompts_repo.update_result(AGENT_NAME, request.prompt_id, PromptStatus.SUCCESS, result)


@api.post("/invoke")
async def invoke(request: AgentInvokeRequest, background_tasks: BackgroundTasks) -> AgentInvokeResponse:
    background_tasks.add_task(invoke_workflow, request)
    return AgentInvokeResponse(prompt_id=request.prompt_id)


@api.post("/task-complete")
async def task_complete(request: TaskCompleteRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(resume_workflow, request)
    return Response(status_code=200)


@api.post("/prompt-result")
async def prompt_result(request: PromptResultRequest):
    try:
        prompts_repo: AgentPromptsRepository = api.state.prompts_repo
        result = await prompts_repo.get_result(AGENT_NAME, request.prompt_id)
        if result:
            status, result_text = result
            return PromptResultResponse(status=status, result=result_text)
        else:
            return Response(status_code=400, content={"message": "Prompt ID not found"})
    except Exception as e:
        logger.error(f"Error while reading prompt result : {str(e)}")
        return Response(status_code=500, content={"message": "Error while reading prompt result"})


class App:

    def __init__(self, workflow: AgentWorkflow):
        api.state.workflow = workflow

    def run(self):
        uvicorn.run(api, host="0.0.0.0", port=8080)