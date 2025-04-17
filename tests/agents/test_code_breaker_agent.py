import pytest
from unittest.mock import patch

from src.agents.code_breaker_agent import CodeBreakerAgent


class TestCodeBreakerAgent:
    possible_numbers = ["1234", "5678", "9201"]

    @pytest.fixture
    def generate_all_4_number_permutations_mock(self):
        with patch(
            "src.agents.code_breaker_agent.generate_all_4_number_permutations"
        ) as unit_service_mock:
            unit_service_mock.return_value = self.possible_numbers.copy()
            yield unit_service_mock

    def test_initialization(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()
        assert agent.possible_numbers is not None
        assert agent.possible_numbers == self.possible_numbers
        assert agent.last_guess is None

        generate_all_4_number_permutations_mock.assert_called_once()

    def test_find_next_guess(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()

        guess = agent._find_next_guess()

        assert guess in self.possible_numbers
        assert agent.last_guess == guess

        agent.possible_numbers = []

        with pytest.raises(
            Exception, match="There are no more possible guesses based on the feedback"
        ):
            agent._find_next_guess()

    def test_calculate_next_guess(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()
        agent.last_guess = "1234"

        agent._calculate_next_guess(1, 1)

        assert agent.possible_numbers == ["9201"]

        agent.possible_numbers = self.possible_numbers.copy()

        agent.last_guess = "5678"
        agent._calculate_next_guess(0, 0)

        assert agent.possible_numbers == ["1234", "9201"]
