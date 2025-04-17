from agents.agent_interface import AgentInterface


class EnvironmentPlayer:
    def __init__(self, id: str, agent: AgentInterface, display_movements: bool = False):
        self.id = id
        self.agent = agent
        self.last_response = None
        self.tries = 0
        self.display_movements = display_movements

    # This method is called by the environment to compute the action.
    # It prints the perception and response of the agent
    # and returns the response.
    def compute_action(self, perception: str) -> str:
        if self.display_movements:
            print(f"{self.id}\tperception: {perception}")

        result = self.agent.compute(perception)

        if self.display_movements:
            print(f"\tresponse: {result}")

        return result
