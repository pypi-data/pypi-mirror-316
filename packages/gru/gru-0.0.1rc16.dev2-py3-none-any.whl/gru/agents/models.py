from pydantic import BaseModel
from typing import Dict, Any

class AgentPromptRequest(BaseModel):
    prompt: Dict[str, Any]
    
class AgentPromptResultRequest(BaseModel):
      prompt_id: str

class AgentRegisterRequest(BaseModel):
	cluster_name: str
	agent_name: str
	image: str
	image_pull_secret: str
	task_server_name: str
	checkpoint_db_name: str
	replicas: int
