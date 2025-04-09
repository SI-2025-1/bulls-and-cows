from agent import Agent

from code_breaker_agent import CodeBreakerAgent
from code_maker_agent import CodeMakerAgent
from enums import PlayerRole, Perceptions


class BullsAndCowsAgent(Agent):
    def __init__(self):
        self.code_breaker = CodeBreakerAgent()
        self.code_maker = CodeMakerAgent()
        self.last_guess = None
        self.role = None
        self.player_id = None

    def _compute(self, perception: str) -> str:
        if perception == Perceptions.WHITE_PLAYER_PERCEPTION.value:
            if self.role:
                raise Exception("Error in perception: role is already assigned")

            # White player starts as the code breaker
            self.role = PlayerRole.CODE_BREAKER
            return Perceptions.BLACK_PLAYER_PERCEPTION.value
        elif perception == Perceptions.BLACK_PLAYER_PERCEPTION.value:
            if self.role:
                raise Exception("Error in perception: role is already assigned")

            # Black player starts as the code maker
            self.role = PlayerRole.CODE_MAKER
            return Perceptions.FIRST_GUESS_PERCEPTION.value
        elif not self.role:
            # Throw an error if the role is not assigned before playing
            raise Exception("Error in perception: role is not assigned")
        elif perception == Perceptions.FIRST_GUESS_PERCEPTION.value:
            # The code maker role should't accept the first guess perception
            if self.role == PlayerRole.CODE_MAKER:
                raise Exception(
                    """Error in perception: the CODE_MAKER
                    doesn't accept the first guess perception"""
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

    # This adds logging capabilities to the _compute function
    # which contains all the agent logic
    def compute(self, perception: str) -> str:
        agent_id = self._get_id_by_perception(perception)
        role = self._get_role_name_by_perception(perception)

        print(f"{agent_id}\trole: {role}")
        print(f"\tperception: {perception}")
        result = self._compute(perception)
        print(f"\tresponse: {result}")

        return result

    def _get_id_by_perception(self, perception: str) -> str:
        if perception == "B":
            self.player_id = "White"
        elif perception == "N":
            self.player_id = "Black"
        return self.player_id

    def _get_role_name_by_perception(self, perception: str) -> str:
        if perception == "B":
            return "CODE BREAKER"
        elif perception == "N":
            return "CODE MAKER"
        return "CODE BREAKER" if self.role == PlayerRole.CODE_BREAKER else "CODE MAKER"
