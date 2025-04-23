from typing import Optional

from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from environments.tournament_match_environment import TournamentMatchEnvironment
from agents.dummy_bulls_and_cows_agent import DummyBullsAndCowsAgent


class TournamentRoundEnvironment(EnvironmentInterface):
    def __init__(self, players: tuple[EnvironmentPlayer]):
        super().__init__(players)

    def run(self, params: tuple = None) -> str:
        matches = self._build_matches()
        results = []

        for match in matches:
            result = match.run(params)

            winner = self._get_winner(result)
            if winner:
                results.append(winner)

        return result.join(",")

    def _get_winner(self, result: str) -> Optional[str]:
        first_match_winner = result.split(",")[0]
        second_match_winner = result.split(",")[1]

        if first_match_winner == "Dummy" or second_match_winner == "Dummy":
            pass
        elif (
            first_match_winner
            and first_match_winner
            and first_match_winner == second_match_winner
        ):
            # One player won both matches
            return first_match_winner
        elif first_match_winner and not second_match_winner:
            # First match has a winner, second match was a draw
            return first_match_winner
        elif not first_match_winner and second_match_winner:
            # First match was a draw, second match has a winner
            return second_match_winner

        return None

    def _build_matches(self) -> list[TournamentMatchEnvironment]:
        current_pair = None
        matches = []

        for player in self.players:
            if current_pair is None:
                current_pair = (player,)
            elif len(current_pair) == 1:
                current_pair = (current_pair[0], player)
                matches.append(TournamentMatchEnvironment(current_pair))
                current_pair = None

        if current_pair is not None:
            dummy_player = EnvironmentPlayer("Dummy", DummyBullsAndCowsAgent())
            matches.append(TournamentMatchEnvironment((current_pair[0], dummy_player)))

        return matches
