from typing import Optional

from bulls_and_cows_agent import BullsAndCowsAgent


class GameEnvironment:
    def __init__(self):
        self.white_player = BullsAndCowsAgent()

        self.black_player = BullsAndCowsAgent()

        self.white_player.compute("B")

        self.black_player.compute("N")

        self.last_white_response = self.white_player.compute("L")
        self.last_black_response = None

        self.current_guesser = "Black"
        self.first_turn = True

    def _play_turn(self) -> Optional[str]:
        if self.current_guesser == "Black":
            black_response = self.black_player.compute(self.last_white_response)

            if self.first_turn:
                winner = self.get_winner()
                if winner:
                    return winner
                self.last_black_response = black_response
                black_response = self.black_player.compute("L")
                self.first_turn = False

            white_response = self.white_player.compute(black_response)
            self.last_white_response = white_response

            self.current_guesser = "White"
        else:
            white_response = self.white_player.compute(self.last_black_response)

            black_response = self.black_player.compute(white_response)
            self.last_black_response = black_response

            self.current_guesser = "Black"

        winner = self.get_winner()
        if winner:
            return winner

    def get_winner(self) -> Optional[str]:
        if "0,4" == self.last_white_response:
            return "Black"
        if "0,4" == self.last_black_response:
            return "White"
        return None

    def run_game(self, max_turns: int = 20) -> str:
        for _ in range(1, max_turns + 1):
            winner = self._play_turn()
            if winner:
                print(f"Agent {winner} has won!")
                return winner
        print("It is a draw")
        return "Draw"
