from agents.agent_interface import AgentInterface


class EnvironmentPlayer:
    def __init__(self, id: str, agent: AgentInterface):
        self.id = id
        self.agent = agent
        self.last_response = None
        self.tries = 0

    # This method is called by the environment to compute the action.
    # It prints the perception and response of the agent
    # and returns the response.
    def compute_action(self, perception: str) -> str:
        print(f"{self.id}\tperception: {perception}")
        result = self.agent.compute(perception)
        print(f"\tresponse: {result}")

        return result
