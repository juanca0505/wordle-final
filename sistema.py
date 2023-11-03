import tkinter as tk
from palabra import Palabra
from juego import Categoria, Jugador, Juego

class Sistema:
    def __init__(self):
        self.categorias = []
        with open("Base_de_datos_palabras_2.txt", "r", encoding='UTF-8') as file:
            line = file.readline().strip("\n").split(",")
            categoria = Categoria(line[1], [])
            while line[0]:
                if categoria.nombre == line[1]:
                    categoria.palabras.append(Palabra(line[0], line[2]))
                else:
                    self.categorias.append(categoria)
                    categoria = Categoria(line[1], [Palabra(line[0], line[2])])
                line = file.readline().strip("\n").split(",")
            self.categorias.append(categoria)

    def mostrar_categorias(self):
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(self.categorias):
            print(f"{i + 1}. {categoria.nombre}")

    def ejecutar(self):
        nombre_jugador = input("Ingresa tu nombre: ")

        self.mostrar_categorias()

        while True:
            try:
                opcion = int(input(f"Selecciona una categoría (1-{len(self.categorias)}): "))
                if 1 <= opcion <= len(self.categorias):
                    break
                else:
                    print("Opción no válida. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada no válida. Ingresa un número válido.")

        categoria_seleccionada = self.categorias[opcion - 1]

        jugador = Jugador(nombre_jugador)
        juego = Juego(jugador, categoria_seleccionada)

        root = tk.Tk()
        interfaz = InterfazWordle(root, juego)
        root.mainloop()

class InterfazWordle:
    def __init__(self, master, juego):
        self.master = master
        self.juego = juego
        self.instrucciones_shown = False
        self.estadisticas_shown = False

        self.master.title("Wordle - Juego")
        self.master.geometry("400x400")

        self.jugador_label = tk.Label(master, text="Jugador: " + juego.jugador.nombre)
        self.jugador_label.pack()

        self.categoria_label = tk.Label(master, text="Categoría: " + juego.categoria.nombre)
        self.categoria_label.pack()

        self.palabra_label = tk.Label(master, text="Ingresa tu palabra:")
        self.palabra_label.pack()

        self.palabra_var = tk.StringVar()
        self.palabra_entry = tk.Entry(master, textvariable=self.palabra_var)
        self.palabra_entry.pack()

        self.intentos_restantes_label = tk.Label(master, text="Intentos restantes: 6")
        self.intentos_restantes_label.pack()

        self.feedback_var = tk.StringVar()
        self.feedback_label = tk.Label(master, textvariable=self.feedback_var)
        self.feedback_label.pack()

        self.intento_button = tk.Button(master, text="Intento", command=self.realizar_intento)
        self.intento_button.pack()

        self.mostrar_instrucciones_button = tk.Button(master, text="Mostrar Instrucciones", command=self.mostrar_instrucciones)
        self.mostrar_instrucciones_button.pack()

        self.mostrar_estadisticas_button = tk.Button(master, text="Mostrar Estadísticas", command=self.mostrar_estadisticas)
        self.mostrar_estadisticas_button.pack()

        self.mostrar_significado_button = tk.Button(master, text="Mostrar Significado", command=self.mostrar_significado)
        self.mostrar_significado_button.pack()

        self.reiniciar_button = tk.Button(master, text="Jugar de Nuevo", command=self.reiniciar_partida)
        self.reiniciar_button.pack()

        self.palabra_entry.bind("<Key>", self.on_entry_key)

    def on_entry_key(self, event):
        if event.char.isdigit():
            return "break"  # No permite ingresar números

    def realizar_intento(self):
        palabra = self.palabra_var.get()
        feedback = self.juego.proporcionar_retroalimentacion(palabra)
        self.feedback_var.set(", ".join(feedback))
        self.juego.jugador.hacer_intento(palabra)
        intentos_restantes = self.juego.jugador.intentos_restantes
        self.intentos_restantes_label.config(text="Intentos restantes: " + str(intentos_restantes))
        self.palabra_var.set("")

        if palabra == self.juego.palabra_objetivo:
            resultado_label = tk.Label(self.master, text="¡Felicidades! Has adivinado la palabra correcta.")
            resultado_label.pack()
            self.juego.jugador.partidas_ganadas += 1
            self.juego.palabra_adivinada = palabra
            self.mostrar_estadisticas_button.config(text="Mostrar Estadísticas\nPartidas Jugadas: {}\nPartidas Ganadas: {}\nPartidas Perdidas: {}\nRacha de Partidas: {}".format(
                self.juego.jugador.partidas_jugadas, self.juego.jugador.partidas_ganadas, self.juego.jugador.partidas_perdidas, self.juego.jugador.racha_partidas))

        if self.juego.jugador.intentos_restantes == 0:
            resultado_label = tk.Label(self.master, text="¡Agotaste todos los intentos! La palabra correcta era '{}'.".format(self.juego.palabra_objetivo))
            resultado_label.pack()
            self.juego.jugador.partidas_perdidas += 1
            self.mostrar_estadisticas_button.config(text="Mostrar Estadísticas\nPartidas Jugadas: {}\nPartidas Ganadas: {}\nPartidas Perdidas: {}\nRacha de Partidas: {}".format(
                self.juego.jugador.partidas_jugadas, self.juego.jugador.partidas_ganadas, self.juego.jugador.partidas_perdidas, self.juego.jugador.racha_partidas))

    def reiniciar_partida(self):
        self.juego.jugador.reiniciar_partida()
        self.juego.palabra_objetivo = self.juego.seleccionar_palabra()
        self.feedback_var.set("")
        self.intentos_restantes_label.config(text="Intentos restantes: 6")
        self.palabra_var.set("")

    def mostrar_instrucciones(self):
        if not self.instrucciones_shown:
            instrucciones_label = tk.Label(self.master, text="Instrucciones del juego:\n"
                                                    "1. Ingresa una palabra de {} letras.\n"
                                                    "2. Presiona 'Intento' para adivinar la palabra.\n"
                                                    "3. Mira la retroalimentación y las estadísticas.".format(len(self.juego.palabra_objetivo))
                                                    )
            instrucciones_label.pack()
            self.instrucciones_shown = True

    def mostrar_estadisticas(self):
        if not self.estadisticas_shown:
            estadisticas_label = tk.Label(self.master, text="Estadísticas\nPartidas Jugadas: {}\nPartidas Ganadas: {}\nPartidas Perdidas: {}\nRacha de Partidas: {}".format(
                self.juego.jugador.partidas_jugadas, self.juego.jugador.partidas_ganadas, self.juego.jugador.partidas_perdidas, self.juego.jugador.racha_partidas))
            estadisticas_label.pack()
            self.estadisticas_shown = True

    def mostrar_significado(self):
        if self.juego.palabra_adivinada:
            significado = ""
            for palabra in self.juego.categoria.palabras:
                if palabra.palabra == self.juego.palabra_adivinada:
                    significado = palabra.significado
                    break

            significado_label = tk.Label(self.master, text="Significado: " + significado)
            significado_label.pack()

if __name__ == "__main__":
    sistema = Sistema()
    sistema.ejecutar()