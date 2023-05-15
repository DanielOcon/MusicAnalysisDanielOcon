from customtkinter import CTkLabel
import threading

# Clase para animar el texto de un CTkLabel
class LoadingAnimation(threading.Thread):
    def __init__(self, label: CTkLabel):
        super().__init__()
        self.label = label
        self._stop_event = threading.Event()

    # Función que se ejecuta cuando se inicia la animación
    def run(self):
        i = 0
        while not self._stop_event.is_set():
            # Texto a animar
            texto = "analizando"
            # Letra a poner en mayúsculas
            letra = texto[i % len(texto)].upper()
            # Nuevo texto con la letra en mayúsculas
            nuevo_texto = texto[:i % len(texto)] + letra + texto[i % len(texto) + 1:]
            # Actualizar el texto del label
            self.label.configure(text=nuevo_texto)
            i += 1
            # Esperar un tiempo antes de actualizar el texto de nuevo
            self._stop_event.wait(0.2)

    # Función para establecer el texto del label sin animación
    def set_label(self, nuevo_texto):
        self.label.configure(text=nuevo_texto)
        self.label.pack()

    # Función para detener la animación
    def stop(self):
        self._stop_event.set()
