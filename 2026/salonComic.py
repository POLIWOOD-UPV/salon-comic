import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_EXTENSIONS = (".mp4",)

# Directorios
videos_root = os.path.join(BASE_DIR, "VIDEOS")
audios_dir = os.path.join(BASE_DIR, "AUDIOS")
output_root = os.path.join(BASE_DIR, "output")
# Logos
LOGO_PW = os.path.join(BASE_DIR, "..", "overlay.png")
LOGO_2 = os.path.join(BASE_DIR, "LOGO", "ASV.jpeg")
LOGO_3 = os.path.join(BASE_DIR, "LOGO", "FREE.png")
LOGO_4 = os.path.join(BASE_DIR, "LOGO", "SC.jpeg")

os.makedirs(output_root, exist_ok=True)

# DEBUG ARCHIIVOS
if not os.path.isdir(videos_root):
    print(f"No existe la carpeta de videos: {videos_root}")
    exit(1)

if not os.path.isdir(audios_dir):
    print(f"No existe la carpeta de audios: {audios_dir}")
    exit(1)

if not os.path.isfile(LOGO_PW):
    print(f"No se encontró el overlay: {LOGO_PW}")
    exit(1)

if not os.path.isfile(LOGO_2):
    print(f"No se encontró el overlay: {LOGO_2}")
    exit(1)

if not os.path.isfile(LOGO_3):
    print(f"No se encontró el overlay: {LOGO_3}")
    exit(1)

if not os.path.isfile(LOGO_4):
    print(f"No se encontró el overlay: {LOGO_4}")
    exit(1)

# Encontrar el audio correspondiente a una carpeta de videos (mismo nombre + .wav)
def find_audio_for_folder(folder_name: str):
    candidate = os.path.join(audios_dir, f"{folder_name}.wav")
    return candidate if os.path.isfile(candidate) else None


# Sacamos los nombres de los audios usando los nombres de las carpetas
video_folders = [
    d for d in os.listdir(videos_root)
    if os.path.isdir(os.path.join(videos_root, d))
]

if not video_folders:
    print(f"No hay carpetas dentro de: {videos_root}")
    exit(1)

processed = 0
skipped = 0

for folder in sorted(video_folders):
    # Coger video
    videos_dir = os.path.join(videos_root, folder)


    # Coger el audio
    audio = find_audio_for_folder(folder)
    if not audio:
        print(f"Saltada carpeta '{folder}': no existe audio con ese nombre en {audios_dir}")
        skipped += 1
        continue

    # Coger los videos dentro de la carpeta
    video_files = [
        f for f in os.listdir(videos_dir)
        if f.lower().endswith(VIDEO_EXTENSIONS) and os.path.isfile(os.path.join(videos_dir, f))
    ]

    if not video_files:
        print(f"Saltada carpeta '{folder}': no hay videos {VIDEO_EXTENSIONS}")
        skipped += 1
        continue


    # Salida
    print(f"\nCarpeta: {folder} | Audio: {os.path.basename(audio)} | Videos: {len(video_files)}")
    
    output_dir = os.path.join(output_root, folder)
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesado de videos
    for file in video_files:
        in_path = os.path.join(videos_dir, file)
        out_path = os.path.join(output_dir, file)

        if os.path.exists(out_path):
            print(f"Saltado (ya existe): {os.path.basename(out_path)}")
            continue

        cmd = [
            "ffmpeg",
            "-y",
            "-i", in_path,              # 0: video
            "-i", LOGO_PW,              # 1: PW
            "-i", LOGO_2,               # 2: ASV
            "-i", LOGO_3,               # 3: FREE
            "-i", LOGO_4,               # 4: SC
            "-stream_loop", "-1",
            "-i", audio,                # 5: audio
            "-filter_complex",
            "[1:v]format=rgba,scale=192:108:force_original_aspect_ratio=decrease[ov1];"
            "[0:v][ov1]overlay=10:H-h-10[paso1];"
            "[2:v]format=rgba,scale=128:128:force_original_aspect_ratio=decrease[ov2];"
            "[paso1][ov2]overlay=W-w-10:H-h-10[paso2];"
            "[3:v]format=rgba,scale=140:140:force_original_aspect_ratio=decrease[ov3];"
            "[paso2][ov3]overlay=10:10[paso3];"
            "[4:v]format=rgba,scale=110:110:force_original_aspect_ratio=decrease[ov4];"
            "[paso3][ov4]overlay=W-w-10:10[vout]",
            "-map", "[vout]",
            "-map", "5:a:0",
            "-shortest",
            "-threads", "1",
            "-filter_threads", "1",
            "-c:v", "libx264",
            "-c:a", "aac",
            out_path,
        ]

        print(">>", " ".join(cmd))
        subprocess.run(cmd, check=True)
        processed += 1
        print(f"Procesado: {folder}/{file} → {os.path.basename(out_path)}")

print(f"\nResumen: procesados={processed}, carpetas saltadas={skipped}")
