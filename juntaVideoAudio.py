import os
import subprocess

# Directorios
audio_dir = "./audio"
video_dir = "./videos"
output_dir = "./output"


#---> AUDIO

# Asegurar que la carpeta de salida existe
os.makedirs(output_dir, exist_ok=True)

# Obtener la lista de archivos de audio
audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
if not audio_files:
    print("No se encontraron archivos de audio.")
    exit(1)

audio_file = audio_files[0]  # Seleccionar el primer archivo de audio encontrado

#---> VIDEO
# Obtener la lista de videos
video_files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]

if not video_files:
    print("No se encontraron archivos de video.")
    exit(1)



#---> PROCESADO
# Procesar cada video
for video_file in video_files:
    input_video = os.path.join(video_dir, video_file)
    input_audio = os.path.join(audio_dir, audio_file)
    output_video = os.path.join(output_dir, video_file)

    # Comando FFmpeg
    cmd = [
        "ffmpeg", "-i", input_video,   # Entrada: Video
        "-stream_loop", "-1",          # Repetir audio infinitamente
        "-i", input_audio,             # Entrada: Audio
        "-shortest",                    # Cortar al menor de los dos
        "-c:v", "copy", "-c:a", "aac",  # Copiar video, convertir audio a AAC
        "-map", "0:v:0", "-map", "1:a:0",  # Seleccionar streams
        output_video                     # Salida
    ]

    # Ejecutar el comando
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Ocultar la salida

print("Procesamiento finalizado.")