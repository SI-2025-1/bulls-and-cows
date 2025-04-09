from agent import Agent
from utils import is_valid_guess, generate_random_secret, calculate_cows_and_bulls


class CodeMakerAgent(Agent):
    def __init__(self):
        self.secret = generate_random_secret()

    def compute(self, perception: str) -> tuple[bool, str]:
        if not is_valid_guess(perception):
            raise ValueError("Invalid perception format")

        cows, bulls = calculate_cows_and_bulls(perception, self.secret)

        return f"{cows},{bulls}"
