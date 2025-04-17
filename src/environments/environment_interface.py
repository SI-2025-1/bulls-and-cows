from abc import abstractmethod
from abc import ABCMeta

from agents.agent_interface import AgentInterface


class EnvironmentInterface(metaclass=ABCMeta):
    def __init__(self, agents: tuple[AgentInterface]):
        self.agents = agents

    @abstractmethod
    def run(self, params: tuple) -> str:
        pass
