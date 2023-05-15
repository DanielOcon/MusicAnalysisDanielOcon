import os
from tkinter import filedialog
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np


class Analizar():

    def __init__(self):
        self.fig, self.axs = plt.subplots(nrows=3, figsize=(12, 6))
        self.texto = ""

    # función que analiza el archivo de audio
    # y devuelve un mensaje con los resultados
    def analyze_music(self, file_path):
        try:
            # Carga el archivo de audio y su tasa de muestreo
            y, sr = librosa.load(file_path, sr=None)

        except ValueError:
            # Si el formato del archivo no es compatible, muestra un mensaje de error
            print("El formato del archivo no es compatible.")
            return

        # Extrae la melodía usando los coeficientes cepstrales de frecuencia mel (MFCC)
        melody = librosa.feature.mfcc(y=y, sr=sr)
        melody_mean = np.mean(melody, axis=1)

        # Calcula el espectrograma de la señal de audio y utiliza una transformada inversa de Fourier para
        # transformar las muestras de señal de audio en el dominio de la frecuencia a espectrogramas de frecuencia
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)

        # Extrae el timbre utilizando el croma de la Constant-Q Transform (CQT) y el tonnetz
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

        # Extrae el tempo y el momento del pulso de la señal de audio utilizando el algoritmo de detección de tempo de librosa
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # Calcula el diagrama cromático de las notas
        chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Calcula el centroide espectral
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)

        # Limpia el primer eje y establece título y etiquetas de los ejes
        self.axs[0].clear()
        self.axs[0].set(title='Waveform', xlabel='Time (seconds)', ylabel='Amplitude')

        # Muestra la forma de onda de la música en el primer eje
        librosa.display.waveshow(y, sr=sr, ax=self.axs[0], alpha=0.8)

        # Limpia el segundo eje y establece título y etiquetas de los ejes
        self.axs[1].clear()
        self.axs[1].set(title='Spectrogram (mel)', xlabel='Time (seconds)', ylabel='Hz')
        librosa.display.specshow(librosa.power_to_db(mel_spec, ref=np.max), y_axis='mel', x_axis='time', ax=self.axs[1],
                                 cmap='magma')

        # Limpia el tercer eje y establece título de los ejes
        self.axs[2].clear()
        self.axs[2].set(title='Chromagram')

        # Muestra un cromagrama de la música en el tercer eje, con escala de colores
        librosa.display.specshow(chromagram, sr=sr, x_axis='time', y_axis='chroma', cmap='coolwarm', ax=self.axs[2])
        # Agrega una barra de color debaro del gráfico del cromagrama
        self.fig.colorbar(self.axs[2].collections[0], ax=self.axs[2], location='bottom')

        # Construye un mensaje con la información extraída y la guarda en la variable de instancia "texto"
        self.texto = "Archivo escaneado: " + file_path + "\n\n\n" \
            + "Tempo: \n" + str(tempo) + "\n\n\n" \
            + "Timbre (Chroma): \n" + Analizar.array_to_string(self, np.mean(chroma, axis=1)) + "\n\n\n" \
            + "Timbre (Tonnetz): \n" + Analizar.array_to_string(self, np.mean(tonnetz, axis=1)) + "\n\n\n" \
            + "Momento del pulso(s): \n" + str(beat_frames) + "\n\n\n" \
            + "Datos del diagrama cromático de las notas: \n" + Analizar.array_to_string(self, np.mean(chroma, axis=1)) + "\n\n\n" \
            + "Datos del espectrograma de la melodía: \n" + Analizar.array_to_string(self, np.mean(melody, axis=1)) + "\n\n\n" \
            + "Datos del centroide espectral: \n" + Analizar.array_to_string(self, np.mean(cent, axis=1)) + "\n\n\n"

        plt.tight_layout()  # Ajusta la disposición de los elementos en la figura
        plt.show()  # Muestra la figura

        # Devuelve el texto generado por la función "analyze_music"
        return self.texto

    # función que elimina los archivos antiguos en un directorio dado
    def delete_old_files(self, dir_path):
        files = os.listdir(dir_path)
        files = [os.path.join(dir_path, f) for f in files]
        files = sorted(files, key=os.path.getctime)
        if len(files) > 1:
            for f in files[:-1]:
                os.remove(f)

    # función que permite al usuario seleccionar un archivo de audio
    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if self.file_path != "":
            if self.file_path.endswith('.mp3') or self.file_path.endswith('.wav'):
                return self.analyze_music(self.file_path)
            else:
                return "No es un archivo compatible."
        else:
            return "No ha seleccionado un archivo válido."

    # función que convierte una matriz en una cadena de texto
    def array_to_string(self, arr):
        result = ""
        for i in range(len(arr)):
            result += str(arr[i])
            if i != len(arr) - 1:
                result += ", "
            if (i + 1) % 5 == 0:
                result += "\n"
        return result


if __name__ == "__main__":
    Analizar()
