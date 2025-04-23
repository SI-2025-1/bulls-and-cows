from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from environments.tournament_match_environment import TournamentMatchEnvironment


class TournamentEnvironment(EnvironmentInterface):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        super().__init__(players)
        self.player_wins = {player.id: 0 for player in players}

    def run(self, params: tuple[int]) -> str:
        rounds = params[0]

        for _ in range(rounds):
            self._play_round()

        sorted_players = self._sort_players_by_score()
        results = [
            f"{player.id}:{self.player_wins[player.id]}" for player in sorted_players
        ]
        return ",".join(results)

    def _play_round(self):
        sorted_players = self._sort_players_by_score()
        match_environment = TournamentMatchEnvironment(sorted_players)
        result = match_environment.run()
        winners = result.split(",")
        for winner in winners:
            self.player_wins[winner] += 1

    def _sort_players_by_score(self):
        return sorted(self.players, key=lambda player: self.player_wins[player.id])
