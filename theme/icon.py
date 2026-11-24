"""Icono de la aplicación (ventana nativa, barra de tareas y pestaña del navegador).

Los archivos viven en `theme/assets/`:

    icon.ico   Windows (ventana + barra de tareas)
    icon.png   Linux
    icon.icns  macOS (opcional)
    icon.svg   favicon cuando se abre en el navegador

Para reemplazarlo por uno propio basta con sobrescribir esos archivos.
"""
from __future__ import annotations

import sys
from pathlib import Path

from nicegui import app

from theme.settings import APP_ID

ASSETS_DIR = Path(__file__).parent / "assets"


def _first_existing(*names: str) -> Path | None:
    for name in names:
        path = ASSETS_DIR / name
        if path.exists():
            return path
    return None


# Favicon para `ui.run(favicon=...)` (pestaña del navegador / modo no nativo).
FAVICON: Path | None = _first_existing("icon.svg", "icon.png", "icon.ico")


def configure_native_window() -> None:
    """Asigna el icono a la ventana nativa. Llamar antes de `ui.run`."""
    if sys.platform == "win32":
        # Sin esto Windows agrupa la ventana bajo "python.exe" y muestra el
        # icono de Python en la barra de tareas.
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
        icon = _first_existing("icon.ico")
    elif sys.platform == "darwin":
        icon = _first_existing("icon.icns", "icon.png")
    else:
        icon = _first_existing("icon.png")

    if icon is not None:
        # `start_args` se pasa tal cual a `webview.start(...)` (pywebview).
        app.native.start_args["icon"] = str(icon)
