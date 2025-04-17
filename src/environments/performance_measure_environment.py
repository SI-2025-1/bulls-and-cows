import math
from multiprocessing import Pool

from environments.environment_interface import EnvironmentInterface
from agents.agent_interface import AgentInterface
from agents.dummy_bulls_and_cows_agent import DummyBullsAndCowsAgent
from environments.bulls_and_cows_environment import BullsAndCowsEnvironment


class PerformanceMeasureEnvironment(EnvironmentInterface):
    MAX_PARALLEL_RUNS = 16

    def __init__(self, agents: tuple[AgentInterface]):
        agent_to_measure = agents[0]

        super().__init__((agent_to_measure, DummyBullsAndCowsAgent()))

        self.bulls_and_cows_environment = BullsAndCowsEnvironment(self.agents)

    def run(self, params: tuple[int]) -> str:
        """Runs a set of games of Bulls and Cows between the
        agent to measure and a dummy agent to measure the
        performance of the agent.

        Receives a tuple of parameters:
        - params[0]: total_runs (int) - The number of games to run.
        - params[1]: max_tries (int) - The maximum number of tries for each game.

        Returns a string with the following format:

        - "min_tries,average_tries,max_tries" where:
            - min_tries: The minimum number of tries taken to win.
            - average_tries: The average number of tries taken to win.
            - max_tries: The maximum number of tries taken to win.
        """

        total_runs, max_tries_per_game = params

        tries_sum = 0
        max_tries = 0
        min_tries = math.inf

        results = self._run_parallel(total_runs, max_tries_per_game)

        for result in results:
            min_tries = min(min_tries, int(result[0]))
            tries_sum += int(result[1])
            max_tries = max(max_tries, int(result[2]))

        average = tries_sum / total_runs

        return f"{min_tries},{average},{max_tries}"

    def _run_parallel(
        self, total_runs: int, max_tries_per_game: int
    ) -> list[tuple[int, int, int]]:
        """Runs the specified number of games in parallel and returns the result list.
        Args:
            total_runs (int): The number of games to run in this chunk.
            max_tries_per_game (int): The maximum number of tries for each game.
        Returns:
            result_ist (list[tuple[int, int, int]]): A list of tuples containing the
            min, sum, and max tries for each chunk.
        """

        results = []
        total_chunks = self.MAX_PARALLEL_RUNS
        chunk_size = total_runs // total_chunks

        try:
            # Create a pool of workers to run the games in parallel
            # and distribute the workload evenly among them
            with Pool(total_chunks) as p:
                results = p.map(
                    self._run_parallel_chunk,
                    [(chunk_size, max_tries_per_game) for _ in range(total_chunks)],
                )
        except KeyboardInterrupt:
            p.terminate() if p else None
        except Exception as e:
            p.terminate() if p else None
            raise e
        finally:
            p.close()
            p.join()

        return results

    def _run_parallel_chunk(self, params: tuple[int, int]) -> tuple[int, int, int]:
        """Runs a chunk of games in parallel and returns the min, sum, and max tries.

        Args:
            params (tuple[int, int]): A tuple containing the number of games to run
            and the maximum number of tries for each game.
        Returns:
            run_results (tuple[int, int, int]): A tuple containing the
            min, sum, and max tries.
        """
        total_runs, max_tries_per_game = params

        tries_sum = 0
        max_tries = 0
        min_tries = math.inf

        for _ in range(total_runs):
            play_result = self.bulls_and_cows_environment.run((max_tries_per_game,))
            _, tries = play_result.split(",")

            tries_sum += int(tries)
            min_tries = min(min_tries, int(tries))
            max_tries = max(max_tries, int(tries))

        return (min_tries, tries_sum, max_tries)
