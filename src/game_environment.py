from typing import Optional

from bulls_and_cows_agent import BullsAndCowsAgent


class GameEnvironment:
    def __init__(self):
        self.white_player = BullsAndCowsAgent()

        self.black_player = BullsAndCowsAgent()

        self.white_player_response = self.white_player.compute("B")
        self.black_player_response = self.black_player.compute("N")

        self.current_guesser = "N"
        self.first_turn = True

    def _play_turn(self) -> Optional[str]:
        if self.current_guesser == "N":
            self.black_player_response = self.black_player.compute(
                self.white_player_response
            )
            print(f"Answer B: {self.black_player_response}")

            self.white_player_response = self.white_player.compute(
                self.black_player_response
            )
            print(f"Answer W: {self.white_player_response}")
            self.current_guesser = "B"

            if self.first_turn:
                self.black_player_response = None
                self.current_guesser = "N"
        else:
            print(f"Guessing B: {self.black_player_response}")
            self.white_player_response = self.white_player.compute(
                self.black_player_response
            )
            print(f"Answer W: {self.white_player_response}")

            print(f"Guessing W: {self.white_player_response}")
            self.black_player_response = self.black_player.compute(
                self.white_player_response
            )
            print(f"Answer B: {self.black_player_response}")

            self.current_guesser = "N"

        if self.black_player_response == "0,4":
            return "White"
        if self.white_player_response == "0,4":
            return "Black"

    def run_game(self, max_turns: int = 20) -> str:
        for _ in range(1, max_turns + 1):
            winner = self._play_turn()
            if winner:
                print(f"Agent {winner} has won!")
                return winner
        print("It is a draw")
        return "Draw"
