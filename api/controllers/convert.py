import mido
import pydub

def convert_mid_to_mp3(mid_file_path, mp3_file_path):
    """
    Convertir un archivo MIDI a MP3.

    Args:
        mid_file_path: La ruta del archivo MIDI de entrada.
        mp3_file_path: La ruta del archivo MP3 de salida.

    Returns:
        None.
    """

    # Leer el archivo MIDI.
    midi = mido.MidiFile(mid_file_path)

    # Crear un objeto AudioSegment a partir del archivo MIDI.
    audio = pydub.AudioSegment.from_midi(midi)

    # Exportar el objeto AudioSegment a MP3.
    audio.export(mp3_file_path, format="mp3")


if __name__ == "__main__":
    # La ruta del archivo MIDI de entrada.
    mid_file_path = "./major-0.mid"

    # La ruta del archivo MP3 de salida.
    mp3_file_path = "my_song.mp3"

    # Convertir el archivo MIDI a MP3.
    convert_mid_to_mp3(mid_file_path, mp3_file_path)
