import random
import re
import itertools

from agents.agent_interface import AgentInterface


class TuringianosAgent(AgentInterface):
    def __init__(self):
        self.mi_numero = mi_numero = "".join(map(str, random.sample(range(10), 4)))
        self.posibles = ["".join(p) for p in itertools.permutations("0123456789", 4)]
        self.intento = random.choice(self.posibles)

    def compute(self, entrada):
        if entrada == "B":
            return "L"

        elif entrada == "N":
            return "L"

        elif entrada == "L":
            return self.intento

        elif re.match(r"^\d,\d$", entrada):
            picas_str, fijas_str = entrada.split(",")
            picas = int(picas_str)
            fijas = int(fijas_str)
            # print(f"Picas: {picas}, Fijas: {fijas}")

            # Filtrar posibles candidatos según picas y fijas
            self.posibles = [
                p
                for p in self.posibles
                if self.calcular_picas_fijas(p, self.intento) == (picas, fijas)
            ]

            # Elegir un nuevo intento
            if self.posibles:
                self.intento = random.choice(self.posibles)

            return self.intento

        elif re.match(r"^\d{4}$", entrada):
            return self.calcular_picas_fijas(entrada, self.mi_numero)

    def calcular_picas_fijas(self, candidato, referencia):
        fijas = sum(a == b for a, b in zip(candidato, referencia))
        picas = (
            sum(min(candidato.count(d), referencia.count(d)) for d in set(candidato))
            - fijas
        )
        return (picas, fijas)
