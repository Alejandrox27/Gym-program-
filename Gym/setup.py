import sys
from cx_Freeze import setup, Executable
import os
from PIL import Image

icon_path = os.path.abspath("icons/icon.ico")
imagen_original = Image.open(icon_path)

nuevo_tamano = (512, 512)
imagen_redimensionada = imagen_original.resize(nuevo_tamano, Image.LANCZOS)
imagen_redimensionada.save("icons/imagen_redimensionada.ico")

imagen_original.close()
imagen_redimensionada.close()
icon_path = os.path.abspath("icons/imagen_redimensionada.ico")


base = None
if sys.platform == "win32":
    base = "Win32GUI"  

options = {
    "build_exe": {
        "packages": ["os", "sys", "PyQt6","email", "smtplib", "re" ,"sqlite3","threading","markdown","datetime","pyperclip"],
        "include_files": ["icons/", "styles/", "GUI/", "models/", "database/"] 
    }
}

executables = [
    Executable("main.py", base=base, icon=icon_path, target_name="Gym")
]

setup(
    name="Gym",
    version="1.0",
    description="Gym program",
    options=options,
    executables=executables
)
#python setup.py build
