from typing import Optional

from common.enums import Perceptions
from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from agents.bulls_and_cows_agent import BullsAndCowsAgent


class BullsAndCowsEnvironment(EnvironmentInterface):
    def __init__(self, agents: tuple[BullsAndCowsAgent]):
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
        if self.current_guesser == self.black_player.id:
            black_response = self.black_player.compute_action(
                self.white_player.last_response
            )

            # Logic for the first turn only
            if self.is_first_turn:
                # If it's the first turn, we need to check if the white player
                # has guessed correctly
                winner = self._check_for_a_winner()
                if winner:
                    return winner

                self.black_player.last_response = black_response

                # Get the first guess from Black at the first turn
                black_response = self.black_player.compute_action(
                    Perceptions.FIRST_GUESS_PERCEPTION.value
                )
                self.is_first_turn = False

            white_response = self.white_player.compute_action(black_response)
            self.white_player.last_response = white_response

            self.current_guesser = "White"

        # White turn to guess
        else:
            white_response = self.white_player.compute_action(
                self.black_player.last_response
            )

            black_response = self.black_player.compute_action(white_response)
            self.black_player.last_response = black_response

            self.current_guesser = "Black"

        # Check if any player has won after the last guess
        winner = self._check_for_a_winner()
        if winner:
            return winner

    def _check_for_a_winner(self) -> Optional[str]:
        if "0,4" == self.white_player.last_response:
            return self.black_player.id
        if "0,4" == self.black_player.last_response:
            return self.white_player.id
        return None
