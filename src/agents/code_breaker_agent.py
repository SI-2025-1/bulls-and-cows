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
        self.last_guess = self._get_next_guess()

    def compute(self, perception: str) -> str:
        if perception == Perceptions.FIRST_GUESS_PERCEPTION.value:
            # Return the first guess
            return self.last_guess

        if not is_valid_feedback(perception):
            raise InvalidPerceptionFormatError()

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

        self.last_guess = self._get_next_guess()
        return self.last_guess

    def _get_next_guess(self) -> str:
        if not self.possible_numbers:
            raise NoPossibleGuessError()

        random_index = random.randint(0, len(self.possible_numbers) - 1)
        return self.possible_numbers[random_index]
