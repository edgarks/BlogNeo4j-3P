"""Punto de entrada: login de conexión a Neo4j (local o Aura) y dashboard CRUD."""
from __future__ import annotations

"""Libreria de interfaz grafica"""
from nicegui import ui

"""Motor de Neo4J para usar Cypher"""
from db import Neo4jService

"""Importar"""
from gui.pages import register_pages

"""Tema (colores, estilos, icono). Ver carpeta /theme"""
from theme import APP_NAME, FAVICON, WINDOW_SIZE, configure_native_window

service = Neo4jService()
register_pages(service)

# [TEMA] Icono de la ventana nativa y de la barra de tareas (theme/assets/icon.ico).
# Se ejecuta a nivel de módulo porque la ventana nativa corre en un proceso hijo
# que vuelve a importar este archivo.
configure_native_window()


if __name__ in {"__main__", "__mp_main__"}:
    # [TEMA] title/favicon/window_size salen de theme/settings.py y theme/assets.
    ui.run(title=APP_NAME, favicon=FAVICON, window_size=WINDOW_SIZE, reload=False, native=True)
"""
title -> Es el titulo de la ventana.
favicon -> Icono de la pestaña (modo navegador). En modo native el icono de la ventana lo pone configure_native_window().
window_size -> Tamaño inicial de la ventana nativa.
reload -> Recarga la aplicación si detecta cambios en el código (programando en True)
native -> Genera una ventana propia en lugar de abrir el navegador en localhost (sigue siendo un navegador empaquetado)
"""
