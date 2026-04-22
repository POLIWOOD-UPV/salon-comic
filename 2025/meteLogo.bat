@echo off
setlocal enabledelayedexpansion

REM ==== Config ====
set "FFMPEG=ffmpeg"
set "VIDEO_DIR=videos"
set "OVERLAY=overlay.png"
set "OUTPUT_DIR=output_logo"
set "X264_PRESET=veryfast"
set "X264_CRF=18"

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

if not exist "%OVERLAY%" (
  echo [ERROR] No se encontro el overlay: "%OVERLAY%"
  exit /b 1
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

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
    -i "%OVERLAY%" ^
    -filter_complex "[1:v]scale=192:108[ovrl];[0:v][ovrl]overlay=10:H-h-10" ^
    -map 0:v:0 -map 0:a? ^
    -c:v libx264 -preset %X264_PRESET% -crf %X264_CRF% -pix_fmt yuv420p ^
    -c:a copy -movflags +faststart ^
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
