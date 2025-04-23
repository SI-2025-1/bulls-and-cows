import random
from itertools import permutations
from agents.agent_interface import AgentInterface


class _404Agent(AgentInterface):
    def __init__(self):
        self.secret_number = ""
        self.guess_candidates = ["".join(p) for p in permutations("0123456789", 4)]
        random.shuffle(self.guess_candidates)
        self.secret_number = "".join(random.sample("0123456789", 4))
        self.last_guess = ""

    def compute(self, entrada: str) -> str:
        if entrada == "B":
            return "L"

        elif entrada == "N":
            return "L"

        elif entrada == "L":
            self.last_guess = self.guess_candidates.pop()
            return self.last_guess

        elif len(entrada) == 4 and entrada.isdigit():
            picas, fijas = self._picas_fijas(entrada, self.secret_number)
            return f"{picas},{fijas}"

        elif "," in entrada:
            try:
                picas, fijas = map(int, entrada.split(","))
                self._filtrar_posibles(picas, fijas)
                if not self.guess_candidates:
                    return "No hay más opciones"
                self.last_guess = self.guess_candidates.pop()
                return self.last_guess
            except:
                return "Formato inválido de picas y fijas (esperado: p,f)"

        return "Entrada no válida"

    def _picas_fijas(self, intento, secreto):
        fijas = sum(a == b for a, b in zip(intento, secreto))
        picas = (
            sum(min(intento.count(d), secreto.count(d)) for d in set(intento)) - fijas
        )
        return picas, fijas

    def _filtrar_posibles(self, picas, fijas):
        def coincide(num):
            p, f = self._picas_fijas(num, self.last_guess)
            return p == picas and f == fijas

        self.guess_candidates = list(filter(coincide, self.guess_candidates))
