"""Ventana principal: navegación entre vistas. Requiere una conexión activa."""
from __future__ import annotations

from nicegui import run, ui

from db import Neo4jService
from gui.views.common import Refresh
from gui.views.registry import VIEWS
from theme import APP_ICON, APP_NAME, apply_theme, theme_toggle


def register(service: Neo4jService) -> None:
    @ui.page("/app")
    async def dashboard_page() -> None:
        if not service.connected:
            ui.navigate.to("/")
            return

        # [TEMA] Colores de marca, CSS global y modo claro/oscuro (theme/core.py).
        dark = apply_theme()

        refreshers: dict[str, Refresh] = {}

        async def disconnect() -> None:
            await run.io_bound(service.close)
            ui.navigate.to("/")

        # ---- Cabecera -------------------------------------------------
        # [TEMA] `app-header`: degradado de cabecera definido en theme/styles.py.
        with ui.header().classes("items-center app-header"):
            ui.icon(APP_ICON, size="md")
            ui.label(APP_NAME).classes("text-h6")
            ui.space()
            # [TEMA] color="positive" usa el verde de la paleta (theme/colors.py).
            ui.badge(f"Conectado: {service.uri}", color="positive")
            # [TEMA] Botón de modo claro/oscuro (blanco sobre la cabecera).
            theme_toggle(dark, props="flat round dense color=white")
            ui.button("Desconectar", icon="power_off", on_click=disconnect).props("flat color=white")

        # ---- Vistas ---------------------------------------------------
        async def on_tab_change(e) -> None:
            refresh = refreshers.get(e.value)
            if refresh:
                await refresh()

        # [TEMA] `app-tabs`: barra de pestañas como tarjeta (theme/styles.py).
        with ui.tabs(on_change=on_tab_change).classes("w-full app-tabs").props(
            "align=left no-caps active-color=primary indicator-color=primary"
        ) as tabs:
            for view in VIEWS:
                ui.tab(view.key, label=view.title, icon=view.icon)

        first = VIEWS[0].key
        with ui.tab_panels(tabs, value=first).classes("w-full"):
            for view in VIEWS:
                with ui.tab_panel(view.key):
                    refreshers[view.key] = view.build(service)

        await ui.context.client.connected()
        await refreshers[first]()
