from environments.performance_measure_environment import PerformanceMeasureEnvironment
from agents.bulls_and_cows_agent import BullsAndCowsAgent


if __name__ == "__main__":
    # Instantiate the agent to measure
    agent_to_measure = BullsAndCowsAgent()

    # Initialize the performance measure environment with the agent to measure
    environment = PerformanceMeasureEnvironment((agent_to_measure,))

    total_runs = 10000
    max_tries_per_game = 10

    print(f"Running {total_runs} games to measure the Agent performance")
    print("Please wait...")

    # Run the performance measure environment with the specified number of runs
    measure_result = environment.run((total_runs, max_tries_per_game))

    # Extract the measurement values from the result string
    min_tries, average_tries, max_tries = measure_result.split(",")

    print("\nPerformance Measure Results:")
    print(f"\tMinimum: {min_tries}")
    print(f"\tAverage: {average_tries}")
    print(f"\tMaximum: {max_tries}")
