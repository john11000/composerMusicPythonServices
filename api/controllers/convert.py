from midi2audio import FluidSynth
from pydub import AudioSegment

# Rutas de los archivos MIDI y WAV
midi_file = "public/1707076033/4-major-C-0.mid"
wav_file = "public/1707076033/4-major-C-0.mid.wav"

# Rutas de los archivos de salida
output_file = 'mezcla.wav'

# Configuración de FluidSynth (puedes necesitar instalar FluidSynth y un soundfont)
fs = FluidSynth()

# Convertir el archivo MIDI a WAV
fs.midi_to_audio(midi_file, 'temp.wav')

# Cargar los archivos WAV utilizando pydub
midi_audio = AudioSegment.from_wav('temp.wav')
wav_audio = AudioSegment.from_wav(wav_file)

# Asegurarse de que ambos archivos tengan la misma frecuencia de muestreo y canales
midi_audio = midi_audio.set_frame_rate(wav_audio.frame_rate)
midi_audio = midi_audio.set_channels(wav_audio.channels)

# Mezclar los archivos WAV
output_audio = midi_audio.overlay(wav_audio)

# Exportar la mezcla a un nuevo archivo WAV
output_audio.export(output_file, format='wav')

# Eliminar el archivo temporal
import os
os.remove('temp.wav')

print(f'Mezcla completa. El archivo de salida se encuentra en: {output_file}')
