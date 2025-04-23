from abc import abstractmethod
from abc import ABCMeta

from environments.environment_player import EnvironmentPlayer


class EnvironmentInterface(metaclass=ABCMeta):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        self.players = players

    @abstractmethod
    def run(self, params: tuple) -> str:
        pass
