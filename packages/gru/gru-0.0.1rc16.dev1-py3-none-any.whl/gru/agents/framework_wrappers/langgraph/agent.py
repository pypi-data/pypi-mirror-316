from typing import Any, Callable
from gru.agents.framework_wrappers import BaseAgent
from langgraph.graph import StateGraph

from gru.agents.framework_wrappers.langgraph.workflow import LanggraphWorkflow
from gru.agents.service.app import App

class CansoLanggraphAgent(BaseAgent):

    def __init__(self, stateGraph: StateGraph, state_result_mapper:Callable[[Any], str] = None) -> None:
        workflow = LanggraphWorkflow(stateGraph, state_result_mapper)
        self.app = App(workflow)

    def run(self):
        self.app.run()

