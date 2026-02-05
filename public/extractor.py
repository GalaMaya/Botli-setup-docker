
import os
import zipfile
import shutil
import brotli
from pathlib import Path

# ===== CONFIG =====
ZIP_FILE = "dummy-game.zip"   # file zip input
GAME_TITLE = "dummy-game"  # folder game di URL
NGINX_GAME_ROOT = "./public/game-list"  # samakan dengan volume docker

# file yang perlu di-brotli
COMPRESS_EXT = {".js", ".wasm", ".data", ".json", ".css", ".html", ".svg", ".txt"}


def extract_zip(zip_path, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest)

    print(f"[OK] Extracted → {dest}")


def brotli_compress_file(file_path):
    br_path = file_path + ".br"

    with open(file_path, "rb") as f:
        data = f.read()

    compressed = brotli.compress(data, quality=5)

    with open(br_path, "wb") as f:
        f.write(compressed)

    print(f"[BR] {file_path} → {br_path}")


def compress_folder(folder):
    for root, _, files in os.walk(folder):
        for name in files:
            file_path = os.path.join(root, name)
            ext = Path(file_path).suffix.lower()

            if ext in COMPRESS_EXT:
                brotli_compress_file(file_path)


def main():
    game_path = os.path.join(NGINX_GAME_ROOT, GAME_TITLE)

    print("=== EXTRACT ===")
    extract_zip(ZIP_FILE, game_path)

    print("=== BROTLI COMPRESS ===")
    compress_folder(game_path)

    print("\nDONE 🚀")
    print(f"Game URL: http://localhost/game-list/{GAME_TITLE}/")


if __name__ == "__main__":
    main()

