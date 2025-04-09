from itertools import permutations
import random

### --------- UTILS --------- ###

def generate_secret():
    """Genera un numero secreto de 4 dígitos no repetidos."""
    digits = random.sample("0123456789", 4)
    return ''.join(digits)

def generate_all_numbers():
    """Genera todos los posibles números 4 dígitos no repetidos."""
    return [''.join(p) for p in permutations("0123456789", 4)]

def validate_guess(guess: str) -> bool:
    """Valida que la conjetura sea de 4 dígitos únicos."""
    return len(guess) == 4 and len(set(guess)) == 4 and guess.isdigit()

def calculate_picas_fijas(candidate: str, guess: str) -> tuple[int, int]:
    """Calcula picas y fijas entre un candidato y una conjetura."""
    picas = sum((d in candidate) and (guess[i] != candidate[i]) for i, d in enumerate(guess))
    fijas = sum(guess[i] == candidate[i] for i in range(4))
    return picas, fijas

def validate_winner(perception: str):
    if ',' in perception:
        picas, fijas = perception.split(',')
        return fijas == '4'
    return False

### --------- CLASES --------- ###

class Agent:
    def __init__(self):
        self.number = generate_secret()  # Número secreto del agente
        self.possible_numbers = generate_all_numbers()  # Posibles números del oponente
        self.last_guess = None  # Última conjetura hecha por este agente
        self.last_action = ""

    def setup(self, perception: str) -> str:
        """Configura el agente según la percepción inicial (B o N)."""
        if perception == 'B':
            return 'N'  # Blanco empieza adivinando
        elif perception == 'N':
            return "L"  # Negro responde "Listo"
        elif perception == 'L':
            return self.send_guess()
        else:
            raise ValueError("Percepción inválida para setup")

    def compute(self, perception: str) -> str:
        """Procesa una percepción y retorna una acción."""
        if perception in "BNL":
            return self.setup(perception)

        if perception == self.last_action:
            print("Percepción Recibida")
            return self.send_guess()

        elif perception.isdigit() and len(perception) == 4:
            # Es un número adivinado por el oponente, calcular picas y fijas
            picas, fijas = calculate_picas_fijas(self.number, perception)
            print(f"Picas, Fijas: {picas}, {fijas}")
            self.last_action =  f"{picas},{fijas}"

        elif ',' in perception:
            # Es feedback (picas, fijas) del oponente
            picas, fijas = map(int, perception.split(','))
            self.process_feedback(picas, fijas)
            self.last_action =  f"{picas},{fijas}"

        else:
            raise ValueError(f"Percepción inválida: {perception}")

        return self.last_action

    def send_guess(self) -> str:
        """Envía una conjetura (número de 4 dígitos)."""
        if not self.possible_numbers:
            raise ValueError("No hay números posibles restantes")
        self.last_guess = random.choice(self.possible_numbers)  # Podría optimizarse
        print(f"Es este tu numero?: {self.last_guess}")
        return self.last_guess

    def process_feedback(self, picas: int, fijas: int) -> None:
        """Filtra los números posibles según el feedback."""
        new_possible = []
        for num in self.possible_numbers:
            computed_p, computed_f = calculate_picas_fijas(num, self.last_guess)
            if computed_p == picas and computed_f == fijas:
                new_possible.append(num)
        self.possible_numbers = new_possible

class Environment:
    def __init__(self, agent_b, agent_n):
        self.agent_b = agent_b  # Agente Blanco (empieza primero)
        self.agent_n = agent_n  # Agente Negro
        self.current_turn = 'B'  # Empieza Blanco
        self.max_turns = 20
        self.winner = None
        self.initialized = False
        self.action = "B"

    def play_turn(self) -> bool:
        """Ejecuta un turno y retorna True si el juego terminó."""
        if not self.initialized:
            self.action = agent_b.compute('B')
            self.current_turn = 'N'
            self.initialized = True

        elif self.current_turn == 'B':
            self.action = agent_b.compute(self.action)
            self.current_turn = 'N'

        elif self.current_turn == 'N':
            self.action = agent_n.compute(self.action)
            self.current_turn = 'B'

        return validate_winner(self.action)

    def run_game(self) -> str:
        """Ejecuta el juego hasta que haya un ganador o se alcance el máximo de turnos."""
        game_over = False
        while not game_over:
            print(f"\n--- Turno ({self.current_turn}) ---")
            game_over = self.play_turn()
            if game_over:
                self.winner = self.current_turn
                print(f"¡Agente {self.winner} ha ganado!")
                return self.winner
        print("¡Empate! Nadie adivinó el número.")
        return "Draw"

# Crear agentes (con métodos vacíos o implementados)
class DummyAgent:

    def __init__(self):
        self.turn = None
        self.number = generate_secret()
        self.last_action = ''

    @staticmethod
    def send_guess():
        return input("Ingresa un número de 4 dígitos: ")

    @staticmethod
    def process_feedback(picas, fijas):
        print(f"Feedback recibido: {picas} picas, {fijas} fijas")

    def setup(self, perception: str) -> str:
        """Configura el agente según la percepción inicial (B o N)."""
        if perception == 'B':
            return 'N'  # Blanco empieza adivinando
        elif perception == 'N':
            return "L"  # Negro responde "Listo"
        elif perception == 'L':
            return self.send_guess()
        else:
            raise ValueError("Percepción inválida para setup")

    def compute(self, perception: str) -> str:
        """Procesa una percepción y retorna una acción."""

        if perception in "BNL":
            return self.setup(perception)

        if perception == self.last_action:
            print("Percepción Recibida")
            return self.send_guess()

        elif perception.isdigit() and len(perception) == 4:
            # Es un número adivinado por el oponente, calcular picas y fijas
            picas, fijas = calculate_picas_fijas(self.number, perception)
            print('Perception received')
            self.last_action = f"{picas},{fijas}"

        elif ',' in perception:
            # Es feedback (picas, fijas) del oponente
            picas, fijas = map(int, perception.split(','))
            self.process_feedback(picas, fijas)
            self.last_action = f"{picas},{fijas}"

        else:
            raise ValueError(f"Percepción inválida: {perception}")

        return self.last_action


# Ejemplo de uso:
if __name__ == "__main__":
    agent_b = Agent()  # Agente Blanco (inicia primero)
    agent_n = Agent()  # Agente Negro
    print(f"Dummy number: {agent_n.number}")
    print(f"Agent number: {agent_b.number}")
    env = Environment(agent_b, agent_n)
    winner = env.run_game()
    print(f"El ganador es: {winner}")