from agents.agent_interface import AgentInterface
from common.utils import (
    generate_all_4_number_permutations,
    is_valid_feedback,
)
from common.enums import Perceptions
from common.errors import InvalidPerceptionFormatError, NoPossibleGuessError


# Dummy agent that guesses by iterating over the list of possible numbers
class DummyCodeBreakerAgent(AgentInterface):
    def __init__(self):
        self.possible_numbers = generate_all_4_number_permutations()
        self.last_guess = None

    def compute(self, perception: str):
        if perception == Perceptions.FIRST_GUESS_PERCEPTION.value:
            return self._calculate_next_guess()

        if not is_valid_feedback(perception):
            raise InvalidPerceptionFormatError()

        _, bulls = map(int, perception.split(","))
        if bulls != 4:
            return self._calculate_next_guess()

        return self.last_guess

    def _calculate_next_guess(self) -> str:
        if not self.possible_numbers:
            raise NoPossibleGuessError()

        self.last_guess = self.possible_numbers.pop(0)
        return self.last_guess
