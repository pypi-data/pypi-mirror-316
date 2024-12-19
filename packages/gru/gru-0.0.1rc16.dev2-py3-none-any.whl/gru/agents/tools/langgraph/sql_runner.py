import os
from typing import Optional, Type
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt

from gru.agents.task_server.celery import TaskMetadata, submit_task
from gru.agents.utils.constants import CANSO_TOOL_INTERRUPT_MESSAGE

class CansoSQLRunnerToolInput(BaseModel):
    query: str = Field(description="sql query to execute")

class CansoSQLRunnerTool(BaseTool):
    name: str = "run_sql_query"
    description: str = "Used to run sql queries on the database"
    args_schema: Type[BaseModel] = CansoSQLRunnerToolInput
    return_direct: bool = True

    class Config:
      extra = 'allow'

    def __init__(self, db_host, db_port, db_username, db_password, db_name):
        super().__init__(
            db_host = db_host,
            db_port = db_port,
            db_username = db_username,
            db_password = db_password,
            db_name = db_name,
        )
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name


    def _run(self, query: str, config: RunnableConfig, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        
        agent_url = os.getenv("AGENT_URL")
        agent_name = os.getenv("AGENT_NAME")

        metadata = TaskMetadata(
            prompt_id = config["metadata"]["thread_id"],
            agent_name = agent_name,
            agent_callback_url = f"http://{agent_url}/task-complete"
        )

        task_attributes = {
            "db_host": self.db_host,
            "db_port" : self.db_port,
            "db_username" : self.db_username,
            "db_password" : self.db_password,
            "db_name" : self.db_name,
            "query": query
        }

        submit_task(self.name, metadata, task_attributes)
        result = interrupt(CANSO_TOOL_INTERRUPT_MESSAGE)

        return result
