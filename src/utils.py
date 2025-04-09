import random
from itertools import permutations


def generate_all_4_number_permutations():
    return ["".join(p) for p in permutations("0123456789", 4)]


def is_valid_guess(guess: str) -> bool:
    return len(guess) == 4 and len(set(guess)) == 4 and guess.isdigit()


def is_valid_feedback(feedback: str) -> bool:
    return (
        feedback
        and len(feedback) == 3
        and feedback[1] == ","
        and feedback[0].isdigit()
        and feedback[2].isdigit()
    )


def generate_random_secret():
    digits = random.sample("0123456789", 4)
    return "".join(digits)


def calculate_cows_and_bulls(secret: str, guess: str) -> tuple[int, int]:
    cows = sum((d in guess) and (secret[i] != guess[i]) for i, d in enumerate(secret))
    bulls = sum(secret[i] == guess[i] for i in range(4))
    return cows, bulls
