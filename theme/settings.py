"""Ajustes generales de identidad visual de la aplicación.

Nombre, icono, tamaño de ventana, tema por defecto y medidas de layout se
cambian aquí, sin tocar las vistas.
"""
from __future__ import annotations

# ---- Identidad -----------------------------------------------------------
APP_NAME = "Blog Neo4j"
# ID único del proceso en Windows: permite que la barra de tareas agrupe la
# ventana bajo NUESTRO icono y no bajo el de "python.exe".
APP_ID = "clabdd.blog.neo4j"
# Icono Material usado en cabecera y login (https://fonts.google.com/icons).
APP_ICON = "hub"

# ---- Ventana nativa ------------------------------------------------------
WINDOW_SIZE = (1280, 800)

# ---- Modo claro/oscuro ---------------------------------------------------
DEFAULT_DARK_MODE = False
# Clave en `app.storage.general` donde se recuerda la elección del usuario.
STORAGE_KEY = "dark_mode"

# ---- Layout y tipografía -------------------------------------------------
RADIUS = "12px"
FONT_FAMILY = (
    '"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Roboto, Arial, sans-serif'
)
