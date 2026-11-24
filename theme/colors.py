"""Paleta de colores de la aplicación.

Hay dos grupos:

* `BRAND`: colores de marca de Quasar (primary, secondary, ...). Se aplican con
  `ui.colors(...)` y los usan los componentes de NiceGUI (`color="primary"`,
  `text-negative`, `bg-positive`, ...). Son iguales en modo claro y oscuro.
* `LIGHT` / `DARK`: colores de superficie (fondo, tarjetas, bordes, texto...).
  Se exponen como variables CSS `--app-*` y cambian solas al alternar el modo
  oscuro, sin recargar la página.
"""
from __future__ import annotations

from dataclasses import dataclass, fields

# ---- Colores de marca (Quasar) --------------------------------------------
BRAND: dict[str, str] = {
    "primary": "#68B1C0",
    "secondary": "#354F7C",
    "accent": "#06B6D4",
    "positive": "#16A34A",
    "negative": "#DC2626",
    "info": "#0EA5E9",
    "warning": "#F59E0B",
    "dark": "#1E293B",
}


@dataclass(frozen=True)
class Palette:
    """Colores de superficie de un modo (claro u oscuro)."""

    background: str      # fondo de la página
    surface: str         # tarjetas, diálogos, tablas, menús
    border: str          # bordes y separadores
    text: str            # texto principal
    text_muted: str      # texto secundario / ayudas
    table_header: str    # fondo de la cabecera de tablas
    row_hover: str       # fila de tabla bajo el cursor
    header_from: str     # degradado de la cabecera (inicio)
    header_to: str       # degradado de la cabecera (fin)
    login_from: str      # degradado de fondo del login (inicio)
    login_to: str        # degradado de fondo del login (fin)

    def css_variables(self) -> str:
        """Devuelve las declaraciones `--app-<nombre>: valor;` de la paleta."""
        return "\n".join(
            f"  --app-{f.name.replace('_', '-')}: {getattr(self, f.name)};"
            for f in fields(self)
        )
UI_CUSTOM = {
    "background_night":"#1F1F1F",
    "surface_night":"#212325",
    "":"",
    "":"",
    "":"",
    "":"",
    "":"",
    "header_from" : "#8DCDDA", #Degradado inicial
   "header_to": "#6E967E"
}

LIGHT = Palette(
    background="#F1F5F9",
    surface="#FFFFFF",
    border="#E2E8F0",
    text="#0F172A",
    text_muted="#64748B",
    table_header="#F8FAFC",
    row_hover="#EEF2FF",
    header_from=UI_CUSTOM["header_from"],
    header_to=UI_CUSTOM["header_to"],
    login_from="#DBEAFE",
    login_to="#EDE9FE",
)

DARK = Palette(
    background=UI_CUSTOM["background_night"],
    surface=UI_CUSTOM["surface_night"],
    border="#414347",
    text="#DCDFDD",
    text_muted="#94A3B8",
    table_header="#212325",
    row_hover="#414247",
    header_from=UI_CUSTOM["header_from"],
    header_to=UI_CUSTOM["header_to"],
    login_from="#212325",
    login_to="#1F1F1F",
)
