from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from environments.bulls_and_cows_environment import BullsAndCowsEnvironment


class TournamentMatchEnvironment(EnvironmentInterface):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        super().__init__(players)

        self.first_play_environment = BullsAndCowsEnvironment(
            (self.players[0], self.players[1])
        )
        self.second_play_environment = BullsAndCowsEnvironment(
            (self.players[1], self.players[0])
        )

    def run(self, params: tuple = None) -> str:
        first_play_results = self.first_play_environment.run(params)
        second_play_results = self.second_play_environment.run(params)

        first_play_winner = first_play_results.split(",")[0]
        second_play_winner = second_play_results.split(",")[0]

        return f"{first_play_winner},{second_play_winner}"
