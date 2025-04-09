from agent import Agent

from code_breaker_agent import CodeBreakerAgent
from code_maker_agent import CodeMakerAgent
from enums import PlayerRole


class BullsAndCowsAgent(Agent):
    def __init__(self):
        self.code_breaker = CodeBreakerAgent()
        self.code_maker = CodeMakerAgent()
        self.last_guess = None
        self.role = None

    def compute(self, perception: str) -> str:
        if perception == "B":
            if self.role:
                raise Exception("Error in perception: role is already assigned")
            self.role = PlayerRole.CODE_BREAKER
            return "N"
        elif perception == "N":
            if self.role:
                raise Exception("Error in perception: role is already assigned")
            self.role = PlayerRole.CODE_MAKER
            return "L"
        elif not self.role:
            raise Exception("Error in perception: role is not assigned")
        elif perception == "L":
            if self.role == PlayerRole.CODE_MAKER:
                raise Exception("Error in perception: it is not a CODE_BREAKER turn")
            self.role = PlayerRole.CODE_MAKER
            return self.code_breaker.compute(perception)
        elif self.role == PlayerRole.CODE_MAKER:
            self.role = PlayerRole.CODE_BREAKER
            return self.code_maker.compute(perception)
        elif self.role == PlayerRole.CODE_BREAKER:
            self.role = PlayerRole.CODE_MAKER
            return self.code_breaker.compute(perception)
