import pytest
from unittest.mock import patch

from src.code_breaker_agent import CodeBreakerAgent


class TestCodeBreakerAgent:
    possible_numbers = ["1234", "5678", "9201"]

    @pytest.fixture
    def generate_all_4_number_permutations_mock(self):
        with patch(
            "src.code_breaker_agent.generate_all_4_number_permutations"
        ) as unit_service_mock:
            unit_service_mock.return_value = self.possible_numbers.copy()
            yield unit_service_mock

    def test_initialization(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()
        assert agent.possible_numbers is not None
        assert agent.possible_numbers == self.possible_numbers
        assert agent.guess is None

        generate_all_4_number_permutations_mock.assert_called_once()

    def test_get_latest_guess(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()

        guess = agent._get_latest_guess()

        assert guess == self.possible_numbers[0]
        assert agent.guess == self.possible_numbers[0]

        agent.possible_numbers = []

        with pytest.raises(Exception, match="Error in perception: no possible numbers"):
            agent._get_latest_guess()

    def test_process_feedback(self, generate_all_4_number_permutations_mock):
        agent = CodeBreakerAgent()
        agent.guess = "1234"

        agent._process_feedback(1, 1)

        assert agent.possible_numbers == ["9201"]

        agent.possible_numbers = self.possible_numbers.copy()

        agent.guess = "5678"
        agent._process_feedback(0, 0)

        assert agent.possible_numbers == ["1234", "9201"]
