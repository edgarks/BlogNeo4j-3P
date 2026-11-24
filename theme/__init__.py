"""Tema de la aplicación: colores, estilos, ajustes e icono.

Uso en una página:

    from theme import apply_theme, theme_toggle

    @ui.page("/")
    def page():
        dark = apply_theme()
        ...
"""
from theme.core import apply_theme, theme_toggle
from theme.icon import FAVICON, configure_native_window
from theme.settings import APP_ICON, APP_NAME, WINDOW_SIZE

__all__ = [
    "APP_ICON",
    "APP_NAME",
    "FAVICON",
    "WINDOW_SIZE",
    "apply_theme",
    "configure_native_window",
    "theme_toggle",
]
