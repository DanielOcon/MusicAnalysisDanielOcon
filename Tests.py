import unittest
import os.path
import webbrowser
import customtkinter as ctk
import main
from Analizar import Analizar
import warnings
from tkinter import Tk
from LoadingAnimation import LoadingAnimation
from unittest.mock import patch

warnings.filterwarnings("ignore", category=ResourceWarning)


class TestAnalizar(unittest.TestCase):

    def setUp(self):
        # Necesario para hacer testing de LoadingAnimation
        self.root = Tk()
        self.label = ctk.CTkLabel(self.root)
        self.analizador = Analizar()
        self.animation = LoadingAnimation(self.label)
        # Nevesario para hacer testing de Analizar
        self.analizar = Analizar()
        # Necesario para hacer testing de main
        self.analysis_results = "dummy analysis results"

    def test_analyze_music_with_valid_file(self):
        file_path = os.path.join("example_data", "Waterflame.wav")
        result = self.analizar.analyze_music(file_path)
        self.assertIsNotNone(result)

    def test_loading_animation_starts_and_stops(self):
        # Crear un objeto LoadingAnimation y asegurarse de que se puede instanciar correctamente
        loading_animation = LoadingAnimation(self.label)

        # Iniciar la animación y asegurarse de que se está ejecutando
        loading_animation.start()
        self.assertTrue(loading_animation.is_alive())

        # Detener la animación y asegurarse de que se ha detenido correctamente
        loading_animation.stop()
        loading_animation.join()
        self.assertFalse(loading_animation.is_alive())

    def test_loading_animation_text_updates(self):
        # Crear un objeto LoadingAnimation y establecer el texto inicial del label
        loading_animation = LoadingAnimation(self.label)
        loading_animation.set_label("analizando")

        # Iniciar la animación y comprobar que el texto del label se actualiza correctamente
        loading_animation.start()
        text = str(self.label.cget("text"))
        self.assertEqual(text.upper(), "analizando".upper())
        loading_animation.stop()

        # Establecer un nuevo texto para el label sin animación y comprobar que se establece correctamente
        loading_animation.set_label("fin")
        self.assertEqual(self.label.cget("text"), "fin")

    @patch.object(webbrowser, 'open')
    def test_help_web(self, mock_open):
        main.help_web()
        mock_open.assert_called_once_with('https://danielocon.github.io/html/help.html')


if __name__ == '__main__':
    unittest.main()
