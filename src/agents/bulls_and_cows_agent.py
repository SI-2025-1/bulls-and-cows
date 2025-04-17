from agents.agent_interface import AgentInterface

from agents.code_breaker_agent import CodeBreakerAgent
from agents.dummy_code_breaker_agent import DummyCodeBreakerAgent
from agents.code_maker_agent import CodeMakerAgent
from common.enums import PlayerRole, Perceptions
from common.errors import UnexpectedPerceptionError, RoleAlreadyAssignedError


class BullsAndCowsAgent(AgentInterface):
    def __init__(self, is_dummy: bool = False):
        self.code_breaker = DummyCodeBreakerAgent() if is_dummy else CodeBreakerAgent()
        self.code_maker = CodeMakerAgent()
        self.last_guess = None
        self.role = None

    def compute(self, perception: str) -> str:
        if perception == Perceptions.WHITE_PLAYER_PERCEPTION.value:
            if self.role:
                raise RoleAlreadyAssignedError()

            # White player starts as the code breaker
            self.role = PlayerRole.CODE_BREAKER
            return Perceptions.BLACK_PLAYER_PERCEPTION.value
        elif perception == Perceptions.BLACK_PLAYER_PERCEPTION.value:
            if self.role:
                raise RoleAlreadyAssignedError()

            # Black player starts as the code maker
            self.role = PlayerRole.CODE_MAKER
            return Perceptions.FIRST_GUESS_PERCEPTION.value
        elif not self.role:
            # Throw an error if the role is not assigned before playing
            raise UnexpectedPerceptionError("No role assigned yet")
        elif perception == Perceptions.FIRST_GUESS_PERCEPTION.value:
            # The code breaker role is the only one that
            # accepts the first guess perception
            if self.role == PlayerRole.CODE_MAKER:
                raise UnexpectedPerceptionError(
                    "the CODE_MAKER doesn't accept the first guess perception"
                )
            self.role = PlayerRole.CODE_MAKER

            # At the first guess, the code breaker accepts a none perception
            return self.code_breaker.compute(perception)
        elif self.role == PlayerRole.CODE_MAKER:
            self.role = PlayerRole.CODE_BREAKER
            return self.code_maker.compute(perception)
        elif self.role == PlayerRole.CODE_BREAKER:
            self.role = PlayerRole.CODE_MAKER
            return self.code_breaker.compute(perception)
