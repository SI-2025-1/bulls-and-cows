import random
from itertools import permutations

from agents.agent_interface import AgentInterface


class LentiumAgent(AgentInterface):
    def __init__(self):
        self.digits = "0123456789"
        self.turno = ""
        self.myNumber = "".join(random.sample(self.digits, 4))
        self.posibles = [
            "".join(p) for p in permutations(self.digits, 4)
        ]  # 5040 posibilidades

    # Acotamos lista de posibles resultados comparando cada numero
    def feedback(self, picas, fijas):
        self.posibles = [
            numero
            for numero in self.posibles
            if self.comparePyF(self.theirNumber, numero) == (picas, fijas)
        ]

    # Comparamos picas y fijas de mi intento contra un posible valor
    def comparePyF(self, guess, numero):
        # Fijas: coincidencias de digito con su posicion
        fijas = 0
        for i in range(4):
            if guess[i] == numero[i]:
                fijas += 1

        # Picas: digitos repetidos entre ambos numero sin importar su posicion
        picas = len(set(guess) & set(numero)) - fijas
        return picas, fijas

    def compute(self, signal: str) -> str:
        if self.turno == "" and signal in ("B", "N"):
            self.turno = signal
            return "L"

        # Primer turno
        if signal == "L":
            self.theirNumber = random.choice(self.posibles)
            return self.theirNumber

        # Si me preguntan (me dan un número de 4 dígitos)
        if len(signal) == 4 and signal.isdigit():
            picas, fijas = self.comparePyF(signal, self.myNumber)
            return f"{picas},{fijas}"

        # Si recibo respuesta (picas,fijas)
        if len(signal) == 3 and "," in signal:
            pyf = signal.split(",")
            picas = int(pyf[0])
            fijas = int(pyf[1])

            self.feedback(picas, fijas)
            self.theirNumber = random.choice(self.posibles)

            return self.theirNumber
