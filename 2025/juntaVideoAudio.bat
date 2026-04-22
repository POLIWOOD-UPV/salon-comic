@echo off
setlocal enabledelayedexpansion

REM ==== Config ====
set "FFMPEG=ffmpeg"
set "VIDEO_DIR=videos"
set "AUDIO_DIR=audio"
set "OUTPUT_DIR=output"

REM ==== Comprobaciones ====
where %FFMPEG% >nul 2>&1
if errorlevel 1 (
  echo [ERROR] ffmpeg no esta en el PATH.
  exit /b 1
)

if not exist "%VIDEO_DIR%" (
  echo [ERROR] No existe la carpeta "%VIDEO_DIR%".
  exit /b 1
)
if not exist "%AUDIO_DIR%" (
  echo [ERROR] No existe la carpeta "%AUDIO_DIR%".
  exit /b 1
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM ==== Seleccionar primer audio ====
set "AUDIO_FILE="
for %%A in ("%AUDIO_DIR%\*.wav" "%AUDIO_DIR%\*.mp3" "%AUDIO_DIR%\*.m4a" "%AUDIO_DIR%\*.aac" "%AUDIO_DIR%\*.flac" "%AUDIO_DIR%\*.ogg") do (
  if exist "%%~A" (
    set "AUDIO_FILE=%%~A"
    goto :audio_found
  )
)
:audio_found

if not defined AUDIO_FILE (
  echo [ERROR] No se encontro ningun archivo de audio en "%AUDIO_DIR%".
  exit /b 1
)

echo Usando audio: "%AUDIO_FILE%"
echo.

REM ==== Procesar videos ====
set /a OK=0
set /a SKIP=0
set /a FAIL=0

for %%V in ("%VIDEO_DIR%\*.mp4") do (
  set "IN=%%~fV"
  set "OUT=%OUTPUT_DIR%\%%~nxV"

  if exist "!OUT!" (
    echo [SKIP] Ya existe: "%%~nxV"
    set /a SKIP+=1
    goto :continueLoop
  )

  echo [RUN ] "%%~nxV"
  "%FFMPEG%" -y ^
    -i "!IN!" ^
    -stream_loop -1 -i "%AUDIO_FILE%" ^
    -shortest -map 0:v:0 -map 1:a:0 ^
    -c:v copy -c:a aac -movflags +faststart ^
    "!OUT!"
  if errorlevel 1 (
    echo [FAIL] "%%~nxV"
    set /a FAIL+=1
  ) else (
    echo [ OK ] "%%~nxV"
    set /a OK+=1
  )
  echo.

  :continueLoop
)

echo Hecho. OK: %OK%  SKIP: %SKIP%  FAIL: %FAIL%
endlocal
