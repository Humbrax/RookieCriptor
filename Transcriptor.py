r"""
Transcriptor interactivo con Whisper (OpenAI)
--------------------------------------------
• Lista los audios en C:\Users\ferna\Desktop\Transcriptor\Audios
• El usuario elige cuál transcribir desde un menú
• Guarda la transcripción en C:\Users\ferna\Desktop\Transcriptor\texto
"""

import os
from pathlib import Path
import openai

# ─── 1. Configuración ──────────────────────────────────────────────────────────
openai.api_key = os.getenv("OPENAI_API_KEY", "TU_CLAVE_API_AQUI")  # ← reemplaza si no usas variable de entorno

AUDIO_DIR  = Path(r"C:\Users\ferna\Desktop\Transcriptor\Audios")
OUTPUT_DIR = Path(r"C:\Users\ferna\Desktop\Transcriptor\texto")
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".wma"}

# Crea la carpeta de salida si no existe
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── 2. Reúne la lista de audios ───────────────────────────────────────────────
audios = sorted([p for p in AUDIO_DIR.iterdir() if p.suffix.lower() in AUDIO_EXTS])

if not audios:
    print(f"⚠️  No se encontraron archivos de audio en: {AUDIO_DIR}")
    raise SystemExit

# ─── 3. Función de transcripción ───────────────────────────────────────────────
def transcribir(audio_path: Path) -> str:
    """Envía un archivo de audio a Whisper y devuelve la transcripción como texto."""
    with audio_path.open("rb") as f:
        respuesta = openai.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="text",
            # language="es"  # Descomenta si deseas forzar español
        )
    return respuesta.strip()

# ─── 4. Menú interactivo ───────────────────────────────────────────────────────
while True:
    print("\n=== Audios disponibles ===")
    for idx, audio in enumerate(audios, start=1):
        print(f"{idx:>2}. {audio.name}")
    print(" 0. Salir")

    try:
        opcion = int(input("\nSeleccione el número del audio a transcribir: "))
    except ValueError:
        print("❌ Entrada inválida. Debe ingresar un número.")
        continue

    if opcion == 0:
        print("👋 Saliendo del transcriptor.")
        break

    if not 1 <= opcion <= len(audios):
        print("❌ Opción fuera de rango. Intente nuevamente.")
        continue

    seleccionado = audios[opcion - 1]
    print(f"\n🎧 Transcribiendo: {seleccionado.name}")

    try:
        texto = transcribir(seleccionado)
    except Exception as e:
        print(f"❌ Error al transcribir {seleccionado.name}: {e}")
        continue

    archivo_salida = OUTPUT_DIR / f"{seleccionado.stem}.txt"
    archivo_salida.write_text(texto, encoding="utf-8")

    print(f"✅ Transcripción guardada en: {archivo_salida}\n")
