from abc import abstractmethod
from abc import ABCMeta


class Agent(metaclass=ABCMeta):
    @abstractmethod
    def compute(self, perception: str) -> str:
        pass
