import random

from agents.agent_interface import AgentInterface
from common.utils import (
    generate_all_4_number_permutations,
    calculate_cows_and_bulls,
    is_valid_feedback,
)
from common.enums import Perceptions
from common.errors import InvalidPerceptionFormatError, NoPossibleGuessError


class CodeBreakerAgent(AgentInterface):
    def __init__(self):
        self.possible_numbers = generate_all_4_number_permutations()
        self.last_guess = None

    def compute(self, perception: str) -> str:
        """Analyzes the feedback and returns the next guess.
        Args:
            perception (str): The feedback from the code maker.
        Returns:
            str: The next guess."""

        if perception == Perceptions.FIRST_GUESS_PERCEPTION.value:
            # Return the first guess
            return self._find_next_guess()

        if not is_valid_feedback(perception):
            raise InvalidPerceptionFormatError(perception)

        cows, bulls = map(int, perception.split(","))
        if bulls != 4:
            return self._calculate_next_guess(cows, bulls)

        return self.last_guess

    # Discards numbers that don't match the feedback
    def _calculate_next_guess(self, cows: int, bulls: int) -> None:
        new_possible_numbers = []
        for candidate in self.possible_numbers:
            computed_cows, computed_bulls = calculate_cows_and_bulls(
                self.last_guess, candidate
            )
            if computed_cows == cows and computed_bulls == bulls:
                new_possible_numbers.append(candidate)
        self.possible_numbers = new_possible_numbers

        return self._find_next_guess()

    def _find_next_guess(self) -> str:
        if not self.possible_numbers:
            raise NoPossibleGuessError()

        random_index = random.randint(0, len(self.possible_numbers) - 1)
        self.last_guess = self.possible_numbers[random_index]
        return self.last_guess
