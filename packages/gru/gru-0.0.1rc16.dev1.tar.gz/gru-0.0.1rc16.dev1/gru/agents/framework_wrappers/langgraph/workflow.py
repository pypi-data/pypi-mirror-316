import json
import os
from typing import Any, Callable

import psycopg
from psycopg_pool import AsyncConnectionPool
from gru.agents.checkpoint.postgres import PostgresAsyncConnectionPool
from gru.agents.framework_wrappers import AgentWorkflow
from langgraph.graph import StateGraph

from gru.agents.schemas import AgentInvokeRequest
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from gru.agents.schemas.schemas import TaskCompleteRequest
from langgraph.types import Command

from gru.agents.utils.constants import CANSO_TOOL_INTERRUPT_MESSAGE

class LanggraphWorkflow(AgentWorkflow):
    
    def __init__(self, stateGraph: StateGraph, state_result_mapper:Callable[[Any], str] = None) -> None:
        super().__init__()
        self.state_graph = stateGraph
        self.state_result_mapper = state_result_mapper

    async def setup(self):
        checkpoint_db_type = os.getenv("CHECKPOINT_DB_TYPE", "postgres")
        if checkpoint_db_type == "postgres":
            pool = PostgresAsyncConnectionPool().get()
            checkpointer = await self._setup_postgres_checkpointer(pool)
            self.compiled_graph = self.state_graph.compile(checkpointer)


    async def invoke(self, request: AgentInvokeRequest) -> tuple[str, bool]:
        config = RunnableConfig(
            configurable={"thread_id": request.prompt_id},
        )
        async for event in self.compiled_graph.astream(input=request.prompt_body, config=config, stream_mode="updates"):
            last_event = event

        processing_complete = False if self._is_canso_tool_interrupt(last_event) else True

        if processing_complete:
            state = await self.compiled_graph.aget_state(config=config)
            result = self.state_result_mapper(state.values) if self.state_result_mapper is not None else str(state.values)
            return result, processing_complete
        else:
            return None, processing_complete
    
    async def resume(self, request: TaskCompleteRequest) -> tuple[str, bool]:
        config = RunnableConfig(
            configurable={"thread_id": request.prompt_id},
        )

        async for event in self.compiled_graph.astream(input=Command(resume=json.dumps(request.result)), config=config, stream_mode="updates"):
            last_event = event

        processing_complete = False if self._is_canso_tool_interrupt(last_event) else True

        if processing_complete:
            state = await self.compiled_graph.aget_state(config=config)
            result = self.state_result_mapper(state.values) if self.state_result_mapper is not None else str(state.values)
            return result, processing_complete
        else:
            return None, processing_complete
    
    async def _setup_postgres_checkpointer(self, pool: AsyncConnectionPool):
        checkpointer = AsyncPostgresSaver(pool)
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE  table_schema = 'public'
                            AND    table_name   = 'checkpoints'
                        );
                    """)
                    table_exists = (await cur.fetchone())[0]
                    
                    if not table_exists:
                        print("Checkpoints table does not exist. Running setup...")
                        await checkpointer.setup()
                    else:
                        print("Checkpoints table already exists. Skipping setup.")
                except psycopg.Error as e:
                    print(f"Error checking for checkpoints table: {e}")
                    raise e
        return checkpointer
    

    def _is_canso_tool_interrupt(self, event) -> bool:

        interrupt_event = event.get("__interrupt__")
        if interrupt_event is not None and interrupt_event[0].value == CANSO_TOOL_INTERRUPT_MESSAGE:
            return True
        
        return False

    
