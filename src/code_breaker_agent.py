from agent import Agent
from utils import (
    generate_all_4_number_permutations,
    calculate_cows_and_bulls,
    is_valid_feedback,
)


class CodeBreakerAgent(Agent):
    def __init__(self):
        self.possible_numbers = generate_all_4_number_permutations()
        self.guess = None

    def compute(self, perception: str = None):
        if not perception:
            return self._get_latest_guess()

        if not is_valid_feedback(perception):
            raise ValueError("Invalid perception format")

        cows, bulls = map(int, perception.split(","))
        if bulls != 4:
            self._process_feedback(cows, bulls)

        return self._get_latest_guess()

    def _get_latest_guess(self) -> str:
        if not self.possible_numbers:
            raise Exception("Error in perception: no possible numbers")

        self.guess = self.possible_numbers[0]
        return self.guess

    def _process_feedback(self, cows: int, bulls: int) -> None:
        new_possible_numbers = []
        for candidate in self.possible_numbers:
            computed_cows, computed_bulls = calculate_cows_and_bulls(
                self.guess, candidate
            )
            if computed_cows == cows and computed_bulls == bulls:
                new_possible_numbers.append(candidate)
        self.possible_numbers = new_possible_numbers
