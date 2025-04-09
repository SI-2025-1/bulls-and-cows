from src.utils import (
    generate_all_4_number_permutations,
    generate_random_secret,
    is_valid_guess,
    calculate_cows_and_bulls,
    is_valid_feedback,
)


class TestUtils:
    def test_generate_all_4_number_permutations(self):
        numbers = generate_all_4_number_permutations()
        assert len(numbers) == 5040
        assert all(len(num) == 4 for num in numbers)
        assert all(num.isdigit() for num in numbers)
        assert all(len(set(num)) == 4 for num in numbers)
        assert len(set(numbers)) == len(numbers)

    def test_is_valid_guess(self):
        assert is_valid_guess("1234") is True
        assert is_valid_guess("1123") is False
        assert is_valid_guess("12345") is False
        assert is_valid_guess("abcd") is False
        assert is_valid_guess("12a4") is False
        assert is_valid_guess("123") is False

        numbers = generate_all_4_number_permutations()
        for num in numbers:
            assert is_valid_guess(num) is True

    def test_is_valid_feedback(self):
        assert is_valid_feedback("1,2") is True
        assert is_valid_feedback("12,3") is False
        assert is_valid_feedback("1,23") is False
        assert is_valid_feedback("1,2,3") is False
        assert is_valid_feedback("a,b") is False
        assert is_valid_feedback("1,2,3") is False

    def test_generate_random_secret(self):
        different_secrets = set()
        for _ in range(100):
            secret = generate_random_secret()
            assert is_valid_guess(secret) is True
            different_secrets.add(secret)

        assert len(different_secrets) > 80, "Secret generation is not random enough"

    def test_calculate_cows_and_bulls(self):
        assert calculate_cows_and_bulls("1234", "5678") == (0, 0)
        assert calculate_cows_and_bulls("1234", "1234") == (0, 4)
        assert calculate_cows_and_bulls("1234", "4321") == (4, 0)
        assert calculate_cows_and_bulls("1234", "1243") == (2, 2)
        assert calculate_cows_and_bulls("1234", "5671") == (1, 0)
