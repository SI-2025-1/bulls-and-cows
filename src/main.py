from environments.bulls_and_cows_environment import BullsAndCowsEnvironment
from agents.bulls_and_cows_agent import BullsAndCowsAgent

# Create a list of agents (players)
agents = (BullsAndCowsAgent(), BullsAndCowsAgent())

# Max number of tries
max_number_of_tries = 20

# Initialize the game environment and start the game
environment = BullsAndCowsEnvironment(agents)
play_result = environment.run([max_number_of_tries])
print(f"Game result: {play_result}")
