"""Aplicación del tema a cada página de NiceGUI."""
from __future__ import annotations

from nicegui import app, ui

from theme.colors import BRAND, DARK
from theme.settings import DEFAULT_DARK_MODE, STORAGE_KEY
from theme.styles import build_css


def apply_theme() -> ui.dark_mode:
    """Aplica colores, CSS y modo claro/oscuro a la página actual.

    Debe llamarse al principio de cada función `@ui.page`. Devuelve el control
    de modo oscuro para poder pasarlo a `theme_toggle`.
    """
    # Colores de marca de Quasar (primary, secondary, ...). `dark_page` es el
    # fondo que Quasar usa en modo oscuro.
    ui.colors(**BRAND, dark_page=DARK.background)
    # Variables CSS `--app-*` y estilos de componentes (ver theme/styles.py).
    ui.add_css(build_css())
    # El modo elegido se recuerda entre ejecuciones (app.storage.general).
    return ui.dark_mode(value=app.storage.general.get(STORAGE_KEY, DEFAULT_DARK_MODE))


def theme_toggle(dark: ui.dark_mode, props: str = "flat round dense") -> ui.button:
    """Botón que alterna entre tema claro y oscuro y guarda la preferencia."""

    def icon_for(value: bool) -> str:
        return "light_mode" if value else "dark_mode"

    def toggle() -> None:
        dark.value = not dark.value
        app.storage.general[STORAGE_KEY] = bool(dark.value)
        button.props(f"icon={icon_for(dark.value)}")

    button = ui.button(icon=icon_for(bool(dark.value)), on_click=toggle).props(props)
    with button:
        ui.tooltip("Cambiar tema claro/oscuro")
    return button
