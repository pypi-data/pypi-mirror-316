from abc import ABC, abstractmethod
from typing import Any

from gru.agents.schemas import AgentInvokeRequest
from gru.agents.schemas.schemas import TaskCompleteRequest


class AgentWorkflow(ABC):

    @abstractmethod
    async def setup(self):
        pass
    
    @abstractmethod
    async def invoke(self, request: AgentInvokeRequest) -> tuple[str, bool]:
        pass

    @abstractmethod
    async def resume(self, request: TaskCompleteRequest) -> tuple[str, bool]:
        pass