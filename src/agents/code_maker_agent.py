from agents.agent_interface import AgentInterface
from common.utils import (
    is_valid_guess,
    generate_random_secret,
    calculate_cows_and_bulls,
)
from common.errors import InvalidPerceptionFormatError


class CodeMakerAgent(AgentInterface):
    def __init__(self):
        self.secret = generate_random_secret()

    def compute(self, perception: str) -> tuple[bool, str]:
        if not is_valid_guess(perception):
            print(perception)
            raise InvalidPerceptionFormatError()

        cows, bulls = calculate_cows_and_bulls(perception, self.secret)

        return f"{cows},{bulls}"
