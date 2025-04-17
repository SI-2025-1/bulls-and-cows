from typing import Optional

from common.enums import Perceptions
from environments.environment_interface import EnvironmentInterface
from environments.environment_player import EnvironmentPlayer
from agents.agent_interface import AgentInterface


class BullsAndCowsEnvironment(EnvironmentInterface):
    DEFAULT_MAX_TRIES = 20

    def __init__(self, agents: tuple[AgentInterface]):
        super().__init__(agents)

    def run(self, params: tuple[int, bool] = None) -> str:
        """Runs a game of Bulls and Cows between two agents.
        The game is played for a maximum number of tries.
        The winner is the player who guesses the secret code first.

        Receives a tuple of parameters:
        - params[0]: max_tries (int) - The maximum number of tries for the game.
        - params[1]: display_game_status (bool) - Whether to display the game status.

        Returns a string with the following format:
        - "White,tries" if White player wins,
        - "Black,tries" if Black player wins,
        - ",max_tries" if it's a draw."""

        # Set the default parameters
        max_tries = self.DEFAULT_MAX_TRIES
        display_game_status = False

        # Set the parameters if provided
        if params:
            max_tries = params[0]
            display_game_status = params[1] if len(params) > 1 else False

        self._prepare(display_game_status)

        # Runs the game for a maximum number of tries
        while (
            self.black_player.tries < max_tries and self.white_player.tries < max_tries
        ):
            game_conclusion = self._play_turn()
            if game_conclusion:
                # If a winner is found, return the result
                winner, tries = game_conclusion
                return f"{winner},{tries}"

        # If no winner is found within the maximum tries, it's a draw
        return f",{max_tries}"

    def _prepare(self, display_game_status: bool) -> None:
        """Prepares the environment for the game to allow doing multiple runs
        within the same instance"""

        # Initialize players
        self.agents[0].__init__()
        self.agents[1].__init__()

        # Instantiate the agents as players
        self.white_player = EnvironmentPlayer(
            "White", self.agents[0], display_game_status
        )
        self.black_player = EnvironmentPlayer(
            "Black", self.agents[1], display_game_status
        )

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

    def _play_turn(self) -> Optional[tuple[str, int]]:
        """Plays a turn of the game. The first turn is played by the white player.
        The game alternates between the two players until one of them wins or
        the maximum number of tries is reached."""

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

    def _check_for_a_winner(self) -> tuple[Optional[str], Optional[str]]:
        """Checks if any player has won the game.
        Returns a tuple with the winner and the number of tries."""

        if "0,4" == self.black_player.last_response:
            return self.white_player.id, self.white_player.tries
        if "0,4" == self.white_player.last_response:
            return self.black_player.id, self.black_player.tries
        return None, None
