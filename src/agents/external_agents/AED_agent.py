import random

from agents.agent_interface import AgentInterface


class AEDAgent(AgentInterface):
    def __init__(self):
        self.juego_empezado = False
        self.soy_blancas = None
        self.intentos_realizados = []
        self.ultima_respuesta = None
        self.posibles = self.generar_todos_los_numeros()
        self.secreto = None

    def generar_todos_los_numeros(self):
        numeros = []
        for a in "0123456789":
            for b in "0123456789":
                if b == a:
                    continue
                for c in "0123456789":
                    if c in (a, b):
                        continue
                    for d in "0123456789":
                        if d in (a, b, c):
                            continue
                        numeros.append(a + b + c + d)
        return numeros

    def generar_numero(self):
        return random.choice(self.posibles)

    def contar_picas_fijas(self, intento, secreto):
        fijas = sum(intento[i] == secreto[i] for i in range(4))
        picas = (
            sum(min(intento.count(d), secreto.count(d)) for d in set(intento)) - fijas
        )
        return f"{picas},{fijas}"

    def compute(self, percepcion):
        if percepcion == "B":
            self.soy_blancas = True
            self.juego_empezado = True
            self.secreto = self.generar_numero()
            return "L"

        elif percepcion == "N":
            self.soy_blancas = False
            self.juego_empezado = True
            self.secreto = self.generar_numero()
            return "L"

        elif percepcion == "L":
            intento = self.generar_numero()
            self.intentos_realizados.append(intento)
            return f"{intento}"

        # elif percepcion.startswith('#'):
        elif len(percepcion) == 4:
            intento = percepcion
            resultado = self.contar_picas_fijas(intento, self.secreto)
            return resultado

        elif "," in percepcion:
            p, f = map(int, percepcion.split(","))
            self.ultima_respuesta = (p, f)

            ultimo_intento = self.intentos_realizados[-1]
            self.posibles = [
                x
                for x in self.posibles
                if self.contar_picas_fijas(ultimo_intento, x) == f"{p},{f}"
            ]
            nuevo_intento = self.posibles[0]
            self.intentos_realizados.append(nuevo_intento)
            return f"{nuevo_intento}"

        return None
