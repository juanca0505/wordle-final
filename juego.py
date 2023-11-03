import random

class Categoria:
    def __init__(self, nombre, palabras):
        self.nombre = nombre
        self.palabras = palabras

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.intentos_restantes = 6
        self.intentos = []
        self.partidas_jugadas = 0
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.racha_partidas = 0

    def hacer_intento(self, palabra):
        self.intentos.append(palabra)
        self.intentos_restantes -= 1

    def reiniciar_partida(self):
        self.intentos_restantes = 6
        self.intentos = []

class Juego:
    def __init__(self, jugador, categoria):
        self.jugador = jugador
        self.categoria = categoria
        self.palabra_objetivo = self.seleccionar_palabra()
        self.palabra_adivinada = None

    def seleccionar_palabra(self):
        return random.choice(self.categoria.palabras).palabra

    def proporcionar_retroalimentacion(self, palabra):
        if len(palabra) != len(self.palabra_objetivo):
            return "La palabra debe tener exactamente {} letras.".format(len(self.palabra_objetivo))

        feedback = []
        for i in range(len(self.palabra_objetivo)):
            if palabra[i] == self.palabra_objetivo[i]:
                feedback.append("verde")
            elif palabra[i] in self.palabra_objetivo:
                feedback.append("amarillo")
            else:
                feedback.append("gris")
        return feedback