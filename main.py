from itertools import permutations
import random

### --------- UTILS --------- ###

def generate_secret():
    """
        Genera un numero secreto de 4 dígitos no repetidos. (Solo 1)
    """
    digits = random.sample("0123456789", 4)
    return ''.join(digits)

def generate_all_numbers():
    """
        Genera todos los posibles números 4 dígitos no repetidos. (5040)
    """
    return [''.join(p) for p in permutations("0123456789", 4)]


def validate_guess(guess: str) -> bool:
    """
        Valída que la conjetura sea de 4 dígitos únicos.
    """
    return len(guess) == 4 and len(set(guess)) == 4 and guess.isdigit()


### --------- CLASES --------- ###

class Agent:
    def __init__(self):
        self.number = generate_secret() # Genera numero aleatorio
        print(f'Secret number: {self.number}')
        self.possible_numbers = generate_all_numbers()
        self.last_guess = None
        self.last_feedback = None
        self.turn = None

    @staticmethod
    def calculate_picas_fijas(candidate: str, guess: str) -> tuple[int, int]:
        """
            Calcula picas y fijas entre un candidato y una conjetura.
        """
        picas = sum((d in candidate) and (guess[i] != candidate[i]) for i, d in enumerate(guess))
        fijas = sum(guess[i] == candidate[i] for i in range(4))
        return picas, fijas

    def compute(self, perception: str):
        """
        Perception: 1 de 4 posibles casos

        Número: 4 Dígitos -> calculate_picas_fijas

        B -> Inicia de primeras
        N -> Inicia de segundas
        """
        if perception == 'B':
            pass
        elif perception == 'N':
            pass
        elif perception.isnumeric() and len(perception) == 4:
            picas, fijas = self.calculate_picas_fijas(perception, self.number)
            return f'{picas},{fijas}'

        elif ',' in perception:
            picas, fijas = map(int,perception.split(','))
            self.process_feedback(picas, fijas)
            return self.send_guess()

        else:
            raise ValueError(f'Perception {perception} invalido')

    ### ---- Envía un número para adivinar ---- ###
    def send_guess(self) -> str:
        if not self.possible_numbers:
            raise Exception('Error in feedback: no posible numbers')

        self.last_guess = self.possible_numbers[0]
        return self.last_guess

    ### ---- Recibe feedback (picas, fijas) del otro agente. ---- ###
    def process_feedback(self, picas: int, fijas: int) -> None:
        """Elimina números imposibles basádo en el feedback."""

        new_possible = []
        for num in self.possible_numbers:
            # Calcula picas/fijas entre `num` y `last_guess`
            computed_p, computed_f = self.calculate_picas_fijas(num, self.last_guess)
            # Conserva solo los números consistentes con el feedback
            if computed_p == picas and computed_f == fijas:
                new_possible.append(num)
        self.possible_numbers = new_possible


    def respond_to_guess(self, guess: str) -> tuple[int, int]:
        """Responde a un número adivinado con (picas, fijas)."""
        # Calcula picas y fijas contra su propio número (self.number)
        picas = sum((d in self.number) and (guess[i] != self.number[i]) for i, d in enumerate(guess))
        fijas = sum(guess[i] == self.number[i] for i in range(4))
        return picas, fijas

from typing import Optional

class Environment:
    def __init__(self, agent_b, agent_n):
        self.agent_b = agent_b  # Agente Blanco (inicia primero)
        self.agent_n = agent_n  # Agente Negro
        self.first_turn = False
        self.turn = 'B'

        self.result_b = None
        self.result_n = None

    def play_turn(self) -> Optional[str]:
        """Ejecuta un turno completo (B -> N o N -> B) y retorna al ganador (B/N) si hay."""
        if self.first_turn:
            self.first_turn = False
            self.result_b = self.agent_b.compute('B')
            self.result_n = self.agent_n.compute('N')
            return
        self.result_b = self.agent_b.compute(self.result_n)
        self.result_n = self.agent_n.compute(self.result_b)


    def run_game(self, max_turns: int = 20) -> str:
        """Ejecuta el juego hasta que haya un ganador o se alcance el máximo de turnos."""
        for turn in range(1, max_turns + 1):
            print(f"\n--- Turno {turn} ({self.current_turn}) ---")
            winner = self.play_turn()
            if winner:
                print(f"¡Agente {winner} ha ganado!")
                return winner
        print("¡Empate! Nadie adivinó el número.")
        return "Draw"

# Crear agentes (con métodos vacíos o implementados)
class DummyAgent:

    def __init__(self):
        self.number = generate_secret()

    @staticmethod
    def send_guess():
        return input("Ingresa un número de 4 dígitos: ")

    @staticmethod
    def process_feedback(picas, fijas):
        print(f"Feedback recibido: {picas} picas, {fijas} fijas")

# Inicializar entorno y agentes
agent_b = DummyAgent()
agent_n = Agent()
env = Environment(agent_b, agent_n)

# Ejecutar juego
env.run_game()