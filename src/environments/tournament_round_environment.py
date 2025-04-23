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

            first_match_winner = result.split(",")[0]
            second_match_winner = result.split(",")[1]
            winner = self._get_winner(first_match_winner, second_match_winner)
            if winner:
                results.append(winner)

        return ",".join(results)

    def _get_winner(
        self, first_match_winner: str, second_match_winner: str
    ) -> Optional[str]:
        has_two_winners = first_match_winner and second_match_winner

        is_a_tie = first_match_winner != second_match_winner

        if first_match_winner == "Dummy" or second_match_winner == "Dummy":
            return None
        elif has_two_winners and not is_a_tie:
            # One player won both matches
            return first_match_winner
        elif has_two_winners and is_a_tie:
            # One player won one match, the other player won the other match
            return f"{first_match_winner}:{second_match_winner}"
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
