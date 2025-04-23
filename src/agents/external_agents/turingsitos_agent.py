import random
from itertools import permutations

from agents.agent_interface import AgentInterface

### --------- CLASES --------- ###


class TuringsitosAgent(AgentInterface):
    def __init__(self):
        super().__init__()
        self.number = self.generate_secret()
        self.last_guess = None  # Última conjetura hecha por este agente
        self.possible_numbers = (
            self.generate_all_numbers()
        )  # Posibles números del oponente

    @staticmethod
    def generate_secret():
        """Genera un numero secreto de 4 dígitos no repetidos."""
        digits = random.sample("0123456789", 4)
        return "".join(digits)

    @staticmethod
    def generate_all_numbers():
        """Genera todos los posibles números 4 dígitos no repetidos."""
        return ["".join(p) for p in permutations("0123456789", 4)]

    @staticmethod
    def calculate_picas_fijas(candidate: str, guess: str) -> tuple[int, int]:
        """Calcula picas y fijas entre un candidato y una conjetura."""
        picas = sum(
            (d in candidate) and (guess[i] != candidate[i]) for i, d in enumerate(guess)
        )
        fijas = sum(guess[i] == candidate[i] for i in range(4))
        return picas, fijas

    def compute(self, perception: str) -> str:
        """Procesa una percepción y retorna una acción."""

        if perception in "BN":
            return "L"

        if perception == "L":
            return self.send_guess()

        elif perception.isdigit() and len(perception) == 4:
            # Es un número adivinado por el oponente, calcular picas y fijas
            picas, fijas = self.calculate_picas_fijas(self.number, perception)
            return f"{picas},{fijas}"

        elif "," in perception:
            # Es feedback (picas, fijas) del oponente
            picas, fijas = map(int, perception.split(","))
            self.process_feedback(picas, fijas)
            return "L"

        else:
            raise ValueError(f"Percepción inválida: {perception}")

    def send_guess(self) -> str:
        """Envía una conjetura (número de 4 dígitos)."""
        if not self.possible_numbers:
            raise ValueError("No hay números posibles restantes")
        self.last_guess = random.choice(self.possible_numbers)  # Podría optimizarse
        return self.last_guess

    def process_feedback(self, picas: int, fijas: int) -> None:
        """Filtra los números posibles según el feedback."""
        new_possible = []
        for num in self.possible_numbers:
            computed_p, computed_f = self.calculate_picas_fijas(num, self.last_guess)
            if computed_p == picas and computed_f == fijas:
                new_possible.append(num)
        self.possible_numbers = new_possible
