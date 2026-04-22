import os
import subprocess

# Directorios
videos_dir = "./videos"
overlay_path = "./overlay.png"
output_dir = "./output_logo"

os.makedirs(output_dir, exist_ok=True)

# Sacar los videos (.mp4 solo)
video_files = [
    f for f in os.listdir(videos_dir)
    if f.lower().endswith(".mp4") and os.path.isfile(os.path.join(videos_dir, f))
]

# Comprobar que los directorios existen
if not video_files:
    print("No se encontraron archivos de video (.mp4).")
    exit(1)

if not os.path.isfile(overlay_path):
    print(f"No se encontró el overlay: {overlay_path}")
    exit(1)

# Procesamos los videos
for file in video_files:
    in_path = os.path.join(videos_dir, file)
    out_path = os.path.join(output_dir, file)

    if os.path.exists(out_path):
        print(f"Saltado (ya existe): {os.path.basename(out_path)}")
        continue

    cmd = [
        "ffmpeg",
        "-y",
        "-i", in_path,            # 0: video
        "-i", overlay_path,       # 1: overlay
        "-filter_complex", "[1:v]scale=192:108[ovrl];[0:v][ovrl]overlay=10:H-h-10",
        "-c:a", "copy",
        out_path
    ]

    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Procesado: {file} → {os.path.basename(out_path)}")
