import sys
import os
import importlib
import types

# Agrega el directorio del ejecutable al path en tiempo de ejecución
if getattr(sys, 'frozen', False):
    # Estamos corriendo en un bundle de PyInstaller
    bundle_dir = sys._MEIPASS
    sys.path.insert(0, bundle_dir)
    
    # Crea un módulo 'src' que apunte al bundle si no existe
    if 'src' not in sys.modules:
        src_module = types.ModuleType('src')
        src_module.__path__ = [bundle_dir]
        sys.modules['src'] = src_module
