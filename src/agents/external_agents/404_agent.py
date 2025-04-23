import random
from itertools import permutations

from agents.agent_interface import AgentInterface


class _404Agent(AgentInterface):
    def __init__(self):
        self.guessing_mode = False
        self.generating_mode = False
        self.secret_number = ""
        self.guess_candidates = []
        self.last_guess = ""

    def compute(self, entrada: str) -> str:
        if entrada == "B":
            self.guessing_mode = True
            self.guess_candidates = ["".join(p) for p in permutations("0123456789", 4)]
            random.shuffle(self.guess_candidates)
            return "L"

        elif entrada == "N":
            self.generating_mode = True
            self.secret_number = "".join(random.sample("0123456789", 4))
            return "L"

        elif entrada == "L":
            if self.guessing_mode and self.guess_candidates:
                self.last_guess = self.guess_candidates.pop()
                return self.last_guess
            elif self.generating_mode:
                return "Listo"
            else:
                return "Modo no iniciado"

        elif len(entrada) == 4 and entrada.isdigit():
            if self.generating_mode:
                picas, fijas = self._picas_fijas(entrada, self.secret_number)
                return f"{picas},{fijas}"
            elif self.guessing_mode:
                self.secret_number = entrada
                return "Listo"
            else:
                return "Modo no iniciado"

        elif "," in entrada and self.guessing_mode:
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


if __name__ == "__main__":
    agente = PicasFijasAgent()
    print("Agente Picas y Fijas con doble rol iniciado.")
    print("Comandos válidos: B, N, L, número (ej. 1234), picas,fijas (ej. 2,1), salir")

    while True:
        entrada = input(">> ").strip()
        if entrada.lower() in ["salir", "exit", "q"]:
            print("Saliendo...")
            break
        salida = agente.compute(entrada)
        print(f"<< {salida}")
