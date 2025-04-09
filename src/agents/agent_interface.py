from abc import abstractmethod
from abc import ABCMeta


class AgentInterface(metaclass=ABCMeta):
    @abstractmethod
    def compute(self, perception: str) -> str:
        pass
