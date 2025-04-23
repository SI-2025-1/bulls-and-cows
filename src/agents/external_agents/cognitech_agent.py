from random import sample
from itertools import combinations, permutations
from time import sleep

from agents.agent_interface import AgentInterface


class CognitechAgent(AgentInterface):
    def __init__(self):
        self.numbers = sample(range(10), k=4)
        self.posibilities = list(combinations(range(10), 4))
        self.potencialUniverses = [[[None] * 4] * 10]
        self.findingPositions = False
        self.guesses = sample(self.posibilities, 1)[0]

    def compute(self, perception: str) -> str:
        if perception == "B":
            self.__init__()
            return "L"
        elif perception == "N":
            self.__init__()
            return "L"
        elif perception == "L":
            return "".join(map(str, self.guesses))

        if len(perception) == 4:
            humanGuess = list(map(int, perception))
            picas, fijas = 0, 0
            for i in range(4):
                fijas += 1 if self.numbers[i] == humanGuess[i] else 0
                picas += 1 if humanGuess[i] in self.numbers else 0
            picas -= fijas
            return f"{picas},{fijas}"
        else:
            picas, fijas = map(int, perception.split(","))
            if len(self.posibilities) == 1:
                self.findingPositions = True
                self.posibilities = list(permutations(self.posibilities[0]))

            if not self.findingPositions:
                self.posibilities = list(
                    filter(
                        lambda x: sum(
                            [1 if self.guesses[i] in x else 0 for i in range(4)]
                        )
                        == (picas + fijas),
                        self.posibilities,
                    )
                )
            else:
                posibilities = self.posibilities.copy()
                self.posibilities = []
                for x in posibilities:
                    potencialPicas = sum(
                        [1 if self.guesses[i] in x else 0 for i in range(4)]
                    )
                    potencialFijas = sum(
                        [1 if self.guesses[i] == x[i] else 0 for i in range(4)]
                    )
                    potencialPicas -= potencialFijas
                    if potencialPicas == picas and potencialFijas == fijas:
                        self.posibilities.append(x)
            self.guesses = sample(self.posibilities, 1)[0]
            return "".join(map(str, self.guesses))


# while True:
#   boy=PicasYFijas()

#   dato=boy.compute(input())

#   print(dato)
