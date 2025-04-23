import random
from collections import Counter
from itertools import permutations

from agents.agent_interface import AgentInterface


class _555Agent(AgentInterface):
    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia el estado del agente para un nuevo juego"""
        self.numsecreto = None
        self.intentos = []
        self.digitos_posibles = list("0123456789")
        self.ultimo_intento = None
        self.digitos_descartados = []
        self.posiciones_confirmadas = [None] * 4

    def calcular_picas_fijas(self, intento):
        """Calcula picas y fijas para un intento contra el número secreto"""
        fijas = sum(s == g for s, g in zip(self.numsecreto, intento))
        comunes = sum((Counter(self.numsecreto) & Counter(intento)).values())
        picas = comunes - fijas
        return f"{picas},{fijas}"

    def compute(self, percepcion):
        """
        Método principal que procesa las entradas y retorna las respuestas apropiadas

        Args:
            percepcion: String con la entrada recibida

        Returns:
            String con la respuesta apropiada según el estado del juego
        """
        # Configuración inicial
        if percepcion in ("B", "N"):
            self.reset()
            self.numsecreto = "".join(random.sample("0123456789", 4))
            return "L"

        # Solicitud de primer intento
        elif percepcion == "L":
            self.ultimo_intento = "".join(random.sample(self.digitos_posibles, 4))
            return f"#{self.ultimo_intento}"

        # Recepción de intento del oponente
        elif len(percepcion) == 4:
            return self.calcular_picas_fijas(percepcion)

        # Recepción de pistas (picas,fijas)
        elif "," in percepcion:
            picas, fijas = map(int, percepcion.split(","))
            self.intentos.append((self.ultimo_intento, picas, fijas))
            self.actualizar_conocimiento(picas, fijas)
            return f"#{self.generar_intento()}"

        # Caso por defecto (no debería ocurrir)
        else:
            return "0,0"

    def generar_intento(self):
        """Genera un nuevo intento basado en el conocimiento acumulado"""
        posibles = []
        for num in self.generar_posibles_numeros():
            valido = True
            for intento, picas, fijas in self.intentos:
                calc_picas, calc_fijas = self.calcular_picas_fijas_para(num, intento)
                if calc_picas != picas or calc_fijas != fijas:
                    valido = False
                    break
            if valido:
                posibles.append(num)

        if posibles:
            self.ultimo_intento = random.choice(posibles)
        else:
            # Fallback si no encuentra números válidos
            self.ultimo_intento = "".join(random.sample(self.digitos_posibles, 4))

        return self.ultimo_intento

    def calcular_picas_fijas_para(self, numero, intento):
        """Calcula picas y fijas para un número hipotético"""
        fijas = sum(s == g for s, g in zip(numero, intento))
        comunes = sum((Counter(numero) & Counter(intento)).values())
        picas = comunes - fijas
        return picas, fijas

    def generar_posibles_numeros(self):
        """Genera todas las permutaciones posibles de 4 dígitos"""
        return ["".join(p) for p in permutations(self.digitos_posibles, 4)]

    def actualizar_conocimiento(self, picas, fijas):
        """Actualiza el conocimiento basado en las pistas recibidas"""
        if picas + fijas == 0:
            # Ningún dígito correcto, descartamos todos
            for d in self.ultimo_intento:
                if d in self.digitos_posibles:
                    self.digitos_posibles.remove(d)
        elif fijas > 0:
            # Algunos dígitos están en la posición correcta
            pass  # Implementación más sofisticada iría aquí
