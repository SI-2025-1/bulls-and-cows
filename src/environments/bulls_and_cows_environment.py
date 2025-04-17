from typing import Optional

from common.enums import Perceptions
from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from agents.agent_interface import AgentInterface


class BullsAndCowsEnvironment(EnvironmentInterface):
    DEFAULT_MAX_TRIES = 20

    def __init__(self, agents: tuple[AgentInterface]):
        super().__init__(agents)

        # Instantiate the agents as players
        self.white_player = EnvironmentPlayer("White", self.agents[0])
        self.black_player = EnvironmentPlayer("Black", self.agents[1])

        # Initialize Black and White players
        self.white_player.compute_action(Perceptions.WHITE_PLAYER_PERCEPTION.value)
        self.black_player.compute_action(Perceptions.BLACK_PLAYER_PERCEPTION.value)

        # Get the first guess from White
        # The last response is used as an input in each turn
        self.white_player.last_response = self.white_player.compute_action(
            Perceptions.FIRST_GUESS_PERCEPTION.value
        )
        self.black_player.last_response = None

        self.current_guesser = self.black_player.id
        self.is_first_turn = True

    def run(self, params: list) -> str:
        max_tries = self.DEFAULT_MAX_TRIES
        # Get the maximum number of tries from the parameters
        if params and len(params) > 0:
            max_tries = params[0]

        # Runs the game for a maximum number of tries
        for _ in range(0, max_tries):
            game_conclusion = self._play_turn()
            if game_conclusion:
                # If a winner is found, return the result
                winner, tries = game_conclusion
                return self._format_result(winner, tries)

        # If no winner is found within the maximum tries, it's a draw
        return "Maximum number of tries reached. No winner."

    def _play_turn(self) -> Optional[tuple[str, int]]:
        # Black turn to guess
        if self.current_guesser == self.black_player.id:
            black_response = self.black_player.compute_action(
                self.white_player.last_response
            )

            # Logic for the first turn only
            if self.is_first_turn:
                # If it's the first turn, we need to check if the white player
                # has guessed correctly
                self.white_player.tries += 1
                winner, tries = self._check_for_a_winner()
                if winner:
                    return winner, tries

                self.black_player.last_response = black_response

                # Get the first guess from Black at the first turn
                black_response = self.black_player.compute_action(
                    Perceptions.FIRST_GUESS_PERCEPTION.value
                )
                self.is_first_turn = False

            white_response = self.white_player.compute_action(black_response)
            self.black_player.tries += 1
            self.white_player.last_response = white_response

            self.current_guesser = self.white_player.id

        # White turn to guess
        else:
            white_response = self.white_player.compute_action(
                self.black_player.last_response
            )

            black_response = self.black_player.compute_action(white_response)
            self.white_player.tries += 1
            self.black_player.last_response = black_response

            self.current_guesser = self.black_player.id

        # Check if any player has won after the last guess
        winner, tries = self._check_for_a_winner()
        if winner:
            return winner, tries

    def _check_for_a_winner(self) -> Optional[str]:
        if "0,4" == self.white_player.last_response:
            return self.black_player.id, self.black_player.tries
        if "0,4" == self.black_player.last_response:
            return self.white_player.id, self.white_player.tries
        return None, None

    def _format_result(self, winner: str, tries: int) -> str:
        return f"{winner} wins in {tries} tries."
