from agents.bulls_and_cows_agent import BullsAndCowsAgent
from environments.environment_player import EnvironmentPlayer
from environments.tournament_environment import TournamentEnvironment

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
from agents.dummy_bulls_and_cows_agent import DummyBullsAndCowsAgent

# from programs import run_performance_measure


def run_tournament():
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
        EnvironmentPlayer("Dummy", DummyBullsAndCowsAgent()),
    ]
    tournament_environment = TournamentEnvironment(players)
    rounds = 20

    result = tournament_environment.run((rounds,))

    print("Tournament Results:")
    print("\n".join(result.split(",")))


if __name__ == "__main__":
    run_tournament()
    # run_performance_measure()
