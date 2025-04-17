from agents.bulls_and_cows_agent import BullsAndCowsAgent


# A dummy bulls and cows agent for testing purposes
class DummyBullsAndCowsAgent(BullsAndCowsAgent):
    def __init__(self):
        super().__init__(is_dummy=True)
