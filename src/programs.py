from environments.performance_measure_environment import PerformanceMeasureEnvironment
from agents.bulls_and_cows_agent import BullsAndCowsAgent
from environments.environment_player import EnvironmentPlayer

from agents.external_agents._404_agent import _404Agent
from agents.external_agents._555_agent import _555Agent
from agents.external_agents.AED_agent import AEDAgent
from agents.external_agents.culiquitacati_agent import CuliquitacatiAgent
from agents.external_agents.fancyai_agent import FancyaiAgent
from agents.external_agents.grupo3_agent import Grupo3Agent
from agents.external_agents.Lentium_agent import LentiumAgent
from agents.external_agents.Turingianos_agent import TuringianosAgent
from agents.external_agents.turingsitos_agent import TuringsitosAgent
from agents.external_agents.cognitech_agent import CognitechAgent


def run_performance_measure_by_agent(player_to_measure: EnvironmentPlayer):
    # Initialize the performance measure environment with the agent to measure
    environment = PerformanceMeasureEnvironment((player_to_measure,))

    total_runs = 10000
    max_tries_per_game = 10

    print(f"Running {total_runs} games to measure the Agent performance")
    print("Please wait...")

    # Run the performance measure environment with the specified number of runs
    measure_result = environment.run((total_runs, max_tries_per_game))

    # Extract the measurement values from the result string
    min_tries, average_tries, max_tries = measure_result.split(",")

    print(f"\nPerformance Measure Results for {player_to_measure.id}:")
    print(f"\tMinimum: {min_tries}")
    print(f"\tAverage: {average_tries}")
    print(f"\tMaximum: {max_tries}")


def run_performance_measure():
    players = [
        EnvironmentPlayer("Jhonatan", BullsAndCowsAgent()),
        EnvironmentPlayer("404", _404Agent()),
        EnvironmentPlayer("555", _555Agent()),
        EnvironmentPlayer("AED", AEDAgent()),
        EnvironmentPlayer("Culiquitacati", CuliquitacatiAgent()),
        EnvironmentPlayer("FancyAI", FancyaiAgent()),
        EnvironmentPlayer("Grupo3", Grupo3Agent()),
        EnvironmentPlayer("Lentium", LentiumAgent()),
        EnvironmentPlayer("Turingianos", TuringianosAgent()),
        EnvironmentPlayer("Turingsitos", TuringsitosAgent()),
        EnvironmentPlayer("Cognitech", CognitechAgent()),
    ]

    for player in players:
        run_performance_measure_by_agent(player)
