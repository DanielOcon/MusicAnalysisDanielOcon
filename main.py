import os
import warnings
import webbrowser
from tkinter import filedialog
import customtkinter as ctk
from Analizar import Analizar
from LoadingAnimation import LoadingAnimation


# Función que agrega el análisis del archivo de audio seleccionado
def add_analisis():
    # Crear una animación de carga
    animacion = LoadingAnimation(label=title_label)
    animacion.start()

    # Llamar a la función "choose_file" del módulo "Analizar" y obtener los resultados
    analysis_results = Analizar.choose_file(self=Analizar())

    # Crear un nuevo objeto "CTkLabel" con el texto obtenido y agregarlo al "scrollable_frame"
    label = ctk.CTkLabel(scrollable_frame, text=analysis_results)
    label.pack()

    # Detener la animación de carga y actualizar la etiqueta de la misma
    animacion.stop()
    animacion.set_label("Resultados del análisis:")

    # Agregar el texto de la etiqueta a una lista
    label_text_list.append(analysis_results)

    # Limpiar el contenido del widget "entry"
    entry.delete(0, ctk.END)


# Esta función guarda los datos analizados en un archivo de texto
def save_data():
    # Se define la ruta de la carpeta donde se guardarán los datos
    dir_path = "data"

    # Si la carpeta no existe, se crea
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Se abre una ventana para que el usuario seleccione la ubicación y el nombre del archivo
    # Se especifica que la extensión por defecto será ".txt"
    # y se muestran dos opciones de filtro de archivo en el cuadro de diálogo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    # Si se ha seleccionado una ubicación y un nombre de archivo, se procede a guardar los datos
    if file_path:
        # Se abre el archivo en modo escritura y se especifica la
        with open(file_path + '.txt', 'w', encoding="utf-8") as f:
            # Se escribe en el archivo los datos contenidos en la lista
            f.write("\n".join(label_text_list))


def help_web():
    # Definir la URL de la página web de ayuda
    url = 'https://danielocon.github.io/html/help.html'

    # Abrir la URL en el navegador predeterminado del usuario
    webbrowser.open(url)


# Esta función añade una nota
def add_nota():
    # Obtiene el texto ingresado en la entrada de texto
    analysis_results = entry.get()

    # Crea una etiqueta de la interfaz gráfica de usuario (GUI) y le asigna el texto ingresado
    label = ctk.CTkLabel(scrollable_frame, text=analysis_results)

    # Empaqueta la etiqueta en el marco desplazable
    label.pack()

    # Agrega el texto de la etiqueta a la lista label_text_list
    label_text_list.append(analysis_results)

    # Borra el texto ingresado en la entrada de texto
    entry.delete(0, ctk.END)


class App(ctk.CTk):
    # es el método constructor de la clase.
    # Se llama automáticamente cuando se crea un nuevo objeto de la clase.
    def __init__(self):
        # super().__init__() llama al constructor de la clase padre (ctk.CTk) para inicializar el objeto.
        super().__init__()


# Creación de la ventana principal y título de la aplicación
if __name__ == "__main__":
    # Crea una nueva ventana de la aplicación utilizando la biblioteca customtkinter
    root = ctk.CTk()
    root.geometry("900x600")
    root.title("Ocón Análisis Musical")

    # Creación de una lista para almacenar las notas
    label_text_list = []

    # Creación de la etiqueta del título
    title_label = ctk.CTkLabel(root, text="Análisis", font=ctk.CTkFont(size=30, weight="bold"))
    title_label.pack(padx=10, pady=(40, 20))

    # Creación de un frame que permite hacer scroll sobre las notas
    scrollable_frame = ctk.CTkScrollableFrame(root, width=750, height=200)
    scrollable_frame.pack()

    # Creación de un campo de entrada para añadir nuevas notas
    entry = ctk.CTkEntry(scrollable_frame, placeholder_text="Añadir nota")
    entry.pack(fill="x")

    # Creación de un botón para iniciar el análisis
    analisis_button = ctk.CTkButton(root, text="Analizar", width=500, command=add_analisis)
    analisis_button.pack(pady=20)

    # Creación de un botón para añadir nuevas notas
    add_button = ctk.CTkButton(root, text="Añadir nota", width=500, command=add_nota)
    add_button.pack(pady=10)

    # Creación de un frame para los botones de guardar datos y ayuda
    button_frame = ctk.CTkFrame(root)
    button_frame.pack()

    # Creación de un botón para guardar los datos
    save_button = ctk.CTkButton(button_frame, text="Guardar Datos", width=250, command=save_data)
    save_button.pack(side="left", padx=10, pady=20)

    # Creación de un botón para abrir la ayuda en una página web
    help_button = ctk.CTkButton(button_frame, text="Ayuda", width=250, command=help_web)
    help_button.pack(side="left", padx=10, pady=20)

    # Ignorar las advertencias
    warnings.filterwarnings("ignore")

    # Ejecución del loop principal de la aplicación
    root.mainloop()
