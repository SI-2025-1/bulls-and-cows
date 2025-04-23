from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from environments.tournament_round_environment import TournamentRoundEnvironment


class TournamentEnvironment(EnvironmentInterface):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        super().__init__(players)
        self.player_wins = {player.id: 0 for player in players}

    def run(self, params: tuple[int]) -> str:
        rounds = params[0]

        for _ in range(rounds):
            self._play_round()

        sorted_players = self._sort_players_by_score(reverse=True)
        results = [
            f"{player.id}: {self.player_wins[player.id]}" for player in sorted_players
        ]
        return ",".join(results)

    def _play_round(self):
        sorted_players = self._sort_players_by_score()
        round_environment = TournamentRoundEnvironment(sorted_players)
        result = round_environment.run()
        winners = result.split(",")
        for winner in winners:
            if ":" in winner:
                # Handle case where two players tie
                winner1, winner2 = winner.split(":")
                self.player_wins[winner1] += 0.5
                self.player_wins[winner2] += 0.5
            elif winner != "":
                self.player_wins[winner] += 1

    def _sort_players_by_score(self, reverse: bool = False) -> list[EnvironmentPlayer]:
        return sorted(
            self.players,
            key=lambda player: self.player_wins[player.id],
            reverse=reverse,
        )
