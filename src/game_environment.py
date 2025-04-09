from typing import Optional

from bulls_and_cows_agent import BullsAndCowsAgent


class GameEnvironment:
    def __init__(self):
        self.white_player = BullsAndCowsAgent()

        self.black_player = BullsAndCowsAgent()

        self.white_player.compute("B")

        self.black_player.compute("N")

        self.round_responses = {
            "Black": [],
            "White": [],
        }

        self.current_guesser = "B"
        self.first_turn = True

    def _play_turn(self) -> Optional[str]:
        if self.current_guesser == "B":
            if self.first_turn:
                last_white_response = self.white_player.compute("L")
            else:
                last_white_response = self.round_responses["White"][-2]

            black_response = self.black_player.compute(last_white_response)
            self.round_responses["Black"].append(black_response)

            if self.first_turn:
                black_response = self.black_player.compute("L")
                self.round_responses["Black"].append(black_response)
                self.first_turn = False

            white_response = self.white_player.compute(black_response)
            self.round_responses["White"].append(white_response)
            self.current_guesser = "N"
        else:
            last_black_response = self.round_responses["Black"][-2]

            white_response = self.white_player.compute(last_black_response)
            self.round_responses["White"].append(white_response)

            black_response = self.black_player.compute(white_response)
            self.round_responses["Black"].append(black_response)

    def get_winner(self) -> Optional[str]:
        if "0,4" in self.round_responses["Black"]:
            return "White"
        if "0,4" in self.round_responses["White"]:
            return "Black"
        return None

    def run_game(self, max_turns: int = 20) -> str:
        for _ in range(1, max_turns + 1):
            winner = self._play_turn()
            if winner:
                print(f"Agent {winner} has won!")
                return winner
        print("It is a draw")
        return "Draw"
