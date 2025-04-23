from itertools import permutations
import random

from agents.agent_interface import AgentInterface


class CuliquitacatiAgent(AgentInterface):
    def __init__(self):
        self.name = "Ag1"
        self.number_original = "".join(map(str, random.sample(list(range(0, 10)), 4)))
        # self.number_original = '2714'

        # Se generan todas las combinaciones válidas de 4 dígitos sin repetir.
        self.all_candidates = ["".join(p) for p in permutations("0123456789", 4)]
        self.history = []  #  historial: [(intento, picas y fijas)]
        self.last_try = None

    def compute(self, perception):
        # Blancas o negras
        if perception == "B":
            return "L"
        elif perception == "N":
            return "L"
        # Llega una L para que el agente proponga/pregunte el primer número
        elif perception == "L":
            return self.act_ask(
                -1
            )  # -1 porque aún no hay historial, no tiene con qué comparar entonces va a preguntar 0123

        # Llega la pregunta/el número del otro agente
        elif len(perception) == 4:
            return self.act_answer(
                perception
            )  # responde con el número de picas y fijas que tiene ese número/percepción

        # Llega el feedback del último número propuesto (picas y fijas)
        elif len(perception) == 3:
            return self.act_ask(
                perception
            )  # vuelve a preguntar pero ahora considerando el historial

    def act_ask(self, picas_y_fijas):
        if picas_y_fijas != -1:
            # Guarda el último intento y la retroalimentación recibida
            self.history.append((self.last_try, picas_y_fijas))
            # Filtra los candidatos que sean compatibles con todo el historial de feedback
            new_candidates = []
            for candidate in self.all_candidates:
                valid = True
                for tried, feedback in self.history:
                    if self.get_feedback(candidate, tried) != feedback:
                        valid = False
                        break
                if valid:
                    new_candidates.append(candidate)
            self.all_candidates = new_candidates

        # Escoge el primer candidato de los filtrados para el siguiente intento
        self.last_try = self.all_candidates[0]
        return self.last_try

    def act_answer(self, number_asked):
        # Calcula picas y fijas comparando el número original con el número recibido
        return self.get_feedback(self.number_original, number_asked)

    def get_feedback(self, secret, guess):
        picas = 0
        fijas = 0
        for i, digit in enumerate(guess):
            if digit == secret[i]:
                fijas += 1
            elif digit in secret:
                picas += 1
        return f"{picas},{fijas}"
