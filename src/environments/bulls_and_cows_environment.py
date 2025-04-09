from typing import Optional

from common.enums import Perceptions
from environments.environment_interface import EnvironmentInterface


class BullsAndCowsEnvironment(EnvironmentInterface):
    def __init__(self, agents):
        super().__init__(agents)

        # Instantiate the agents as players
        self.white_player = self.agents[0]
        self.black_player = self.agents[1]

        # Initialize Black and White players
        self.white_player.compute(Perceptions.WHITE_PLAYER_PERCEPTION.value)
        self.black_player.compute(Perceptions.BLACK_PLAYER_PERCEPTION.value)

        # Get the first guess from White
        # The last response is used as an input in each turn
        self.last_white_response = self.white_player.compute(
            Perceptions.FIRST_GUESS_PERCEPTION.value
        )
        self.last_black_response = None

        self.current_guesser = "Black"
        self.first_turn = True

    def run(self, params: list) -> str:
        max_tries = params[0]

        # Runs the game for a maximum number of tries
        for _ in range(1, max_tries + 1):
            winner = self._play_turn()
            if winner:
                print(f"Agent {winner} has won!")
                return winner

        # If no winner is found within the maximum tries, it's a draw
        print("It is a draw")
        return "Draw"

    def _play_turn(self) -> Optional[str]:
        # Black turn to guess
        if self.current_guesser == "Black":
            black_response = self.black_player.compute(self.last_white_response)

            # Logic for the first turn only
            if self.first_turn:
                # If it's the first turn, we need to check if the white player
                # has guessed correctly
                winner = self._get_winner()
                if winner:
                    return winner

                self.last_black_response = black_response

                # Get the first guess from Black at the first turn
                black_response = self.black_player.compute(
                    Perceptions.FIRST_GUESS_PERCEPTION.value
                )
                self.first_turn = False

            white_response = self.white_player.compute(black_response)
            self.last_white_response = white_response

            self.current_guesser = "White"

        # White turn to guess
        else:
            white_response = self.white_player.compute(self.last_black_response)

            black_response = self.black_player.compute(white_response)
            self.last_black_response = black_response

            self.current_guesser = "Black"

        # Check if any player has won after the last guess
        winner = self._get_winner()
        if winner:
            return winner

    def _get_winner(self) -> Optional[str]:
        if "0,4" == self.last_white_response:
            return "Black"
        if "0,4" == self.last_black_response:
            return "White"
        return None
