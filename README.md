# Salón del Cómic 2024

Código para **sincronizar videos y audios** de la colaboración **American Space x POLIWOOD** en el Salón del Cómic 2024.

---

## 📖 Introducción
Durante la colaboración grabamos varios vídeos en pantalla verde para luego reemplazar el fondo por imágenes personalizadas.  
Cada fondo tenía un **audio específico** asociado.  

Para unirlos creamos un script en Python que usa **ffmpeg**:  
- Un script junta **vídeo + audio**. *juntaVideoAudio.py* 
- Otro script añade el **logo de POLIWOOD** en la esquina inferior izquierda, en los vídeos que aún no lo tenían. *meteLogo.py*

---

## ⚙️ Requisitos
- [Python 3](https://www.python.org/downloads/)  
- [ffmpeg](https://ffmpeg.org/download.html) (debe estar en el `PATH`)  

---

## 📂 Estructura de carpetas

Coloca los archivos de esta forma:

```bash
.
├── videos/        # vídeos originales sin audio
├── audio/         # audios a usar
├── overlay.png    # Overlay del logo de PW
├── script.py      # Script que vayas a ejecutar
├── output/        # se crea automáticamente con los resultados
```

---

## 🚀 Uso
1. Copia los **vídeos** en la carpeta `videos/`.  
2. Copia los **audios** en la carpeta `audio/`.  
3. Ejecuta el script que necesites:  

   - Para **juntar audio y vídeo**:  
     ```bash
     python script.py
     ```  

   - Para **añadir el logo** a los vídeos:  
     ```bash
     python logo.py
     ```

4. Los resultados aparecerán en la carpeta `output/`.


---

## 💡 Alternativa en Windows (.bat)
Si no quieres usar Python, también incluimos dos scripts `.bat` que hacen lo mismo directamente con **ffmpeg**:

- `join_audio.bat` → une cada vídeo con el primer audio de `audio/` (lo repite en bucle si es necesario).  
- `add_logo.bat` → añade el logo `overlay.png` en la esquina inferior izquierda de todos los vídeos.  

### Uso
1. Coloca los archivos en la misma estructura de carpetas (`videos/`, `audio/`, `overlay.png`).  
2. Ejecuta el `.bat` correspondiente haciendo doble clic o desde consola:  

   ```bash
   join_audio.bat
   add_logo.bat
   ```


---

## ⚠️ Atención
- El script de audio usa **solo el primer audio** que encuentre dentro de `./audio/`.  
- Ambos scripts leen siempre de `./videos/` y escriben en `./output/`, lo que permite usarlos de forma independiente y flexible.  

---

## Notas
- Si un vídeo ya existe en `output/`, no se vuelve a procesar.  
- El vídeo mantiene su pista de audio original solo cuando usas el script de logo.  
- El logo se aplica en la esquina **inferior izquierda** con tamaño fijo.
