from itertools import permutations
from random import choice

from agents.agent_interface import AgentInterface


class FancyaiAgent(AgentInterface):
    def __init__(self):
        self.secret_number = None
        self.guess = None
        self.picas = 0
        self.fijas = 0
        self.posibilities = [
            "".join(map(str, perm)) for perm in permutations("0123456789", 4)
        ]
        self.historial = []  # guarda pares (guess, respuesta)
        self.ready_to_guess = False  # B
        self.ready_to_answer = False  # Ya genero el n secreto?

    def generate_number(self):
        return choice(self.posibilities)

    def count_picas_fijas(self, guess, aim=None):
        aim = aim or self.secret_number
        picas = sum(1 for i in range(4) if guess[i] in aim and guess[i] != aim[i])
        fijas = sum(1 for i in range(4) if guess[i] == aim[i])
        return picas, fijas

    def compute(self, percepcion: str) -> str:
        if percepcion == "B":
            self.ready_to_guess = True
            self.ready_to_answer = True
            # Crea su numero secreto
            self.secret_number = None
            # Crea su intento inicial
            self.guess = self.generate_number()
            self.posibilities.remove(self.guess)
            self.historial = []
            return "L"

        elif percepcion == "N":
            self.ready_to_answer = True
            self.secret_number = self.generate_number()
            return "L"

        elif percepcion == "L":
            if self.guess is None:
                self.guess = self.generate_number()
                self.posibilities.remove(self.guess)
            return self.guess

        elif "," in percepcion:
            ## recibe respuesta
            picas, fijas = map(int, percepcion.split(","))
            self.historial.append(
                (self.guess, (picas, fijas))
            )  # se agrega el intento y sus respectivas picas

            if fijas == 4:
                return "L"

            self.posibilities = [
                p
                for p in self.posibilities
                if all(
                    self.count_picas_fijas(p, prev_guess) == resultado
                    for prev_guess, resultado in self.historial
                )
            ]
            if self.posibilities:
                self.guess = choice(self.posibilities)
            return self.guess

        elif percepcion.isdigit() and len(percepcion) == 4:
            if self.secret_number:
                picas, fijas = self.count_picas_fijas(percepcion)
                return f"{picas},{fijas}"

        return "L"  # Por si acaso
        # def reset_game(self):
        #     self.__init__()


class Environment:
    def __init__(self, blanco, negro):
        self.blanco = blanco
        self.negro = negro
        self.turno = "B"
        self.winner = None

    def start(self):
        # Verifica que los dos agentes esten listos para jugar
        if self.blanco.compute("B") == "L" and self.negro.compute("N") == "L":
            print("El juego ha iniciado")
            while self.winner is None:
                # Juega los turnos del agente blanco y negro
                if self.turno == "B":
                    print("Turno de blanco")
                    guess = self.blanco.compute("L")
                    print(f"Blanco adivina: {guess}")
                    picas_fijas = self.negro.compute(guess)
                    print(f"Negro responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "B"
                    self.blanco.compute(picas_fijas)
                    self.turno = "N"
                else:
                    print("Turno de Negro")
                    guess = self.negro.compute("L")
                    print(f"Negro adivina: {guess}")
                    picas_fijas = self.blanco.compute(guess)
                    print(f"Blanco responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "N"
                    self.negro.compute(picas_fijas)
                    self.turno = "B"
        else:
            print("Hay un error el juego no puede comenzar")

    def get_winner(self):
        if self.winner == "B":
            print("El ganador es el Blanco")
        elif self.winner == "N":
            print("El ganador es el Negro")
        else:
            print("Hay un error")


if __name__ == "__main__":
    agente_1 = AgentePicasFijas()
    agente_2 = AgentePicasFijas()
    print("=" * 50)
    print("Primer juego: Agente 1 con Blancas")
    game_1 = Environment(agente_1, agente_2)
    game_1.start()
    game_1.get_winner()
    print("=" * 50)
    print("Segundo juego: Agente 2 con Blancas")
    agente_1 = AgentePicasFijas()
    agente_2 = AgentePicasFijas()
    game_2 = Environment(agente_2, agente_1)
    game_2.start()
    game_2.get_winner()
