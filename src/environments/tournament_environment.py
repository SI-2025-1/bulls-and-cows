from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer


class TournamentEnvironment(EnvironmentInterface):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        pass

    def run(self, params: tuple[int]) -> str:
        pass
