"""Pantalla inicial: formulario de conexión a Neo4j (local o Aura)."""
from __future__ import annotations

import os

from nicegui import run, ui

from db import Neo4jService
from theme import APP_ICON, APP_NAME, apply_theme, theme_toggle

LOCAL_URI = "neo4j://127.0.0.1:7687"
AURA_URI = "neo4j+s://<id-instancia>.databases.neo4j.io"

HINTS = {
    "local": "Local: neo4j://127.0.0.1:7687 (Neo4j Desktop / Docker / servidor propio).",
    "aura": "Aura: usa la URI neo4j+s://... y las credenciales de tu instancia.",
}


def register(service: Neo4jService) -> None:
    @ui.page("/")
    def login_page() -> None:
        if service.connected:
            ui.navigate.to("/app")
            return

        # [TEMA] Colores de marca, CSS global y modo claro/oscuro (theme/core.py).
        dark = apply_theme()
        # [TEMA] Fondo degradado del login: clase `app-login-bg` sobre <body> (theme/styles.py).
        ui.query("body").classes("app-login-bg")

        # [TEMA] Botón de modo oscuro fijo en la esquina superior derecha.
        with ui.page_sticky(position="top-right", x_offset=16, y_offset=16):
            theme_toggle(dark, props="flat round")

        with ui.column().classes("w-full min-h-screen items-center justify-center"):
            # [TEMA] `app-login-card`: sombra pronunciada; el resto lo da el estilo global de q-card.
            with ui.card().classes("w-full max-w-md gap-3 app-login-card"):
                with ui.row().classes("items-center"):
                    ui.icon(APP_ICON, size="md", color="primary")
                    ui.label(APP_NAME).classes("text-h5")
                # [TEMA] `app-muted` sustituye a `text-grey` (se adapta al modo oscuro).
                ui.label("Conecta con tu base de datos para continuar.").classes("app-muted")

                mode = ui.toggle({"local": "Local", "aura": "Neo4j Aura"}, value="local")
                uri = ui.input("URI", value=os.getenv("NEO4J_URI", LOCAL_URI)).classes("w-full")
                hint = ui.label(HINTS["local"]).classes("text-caption app-muted")
                user = ui.input("Usuario", value=os.getenv("NEO4J_USER", "neo4j")).classes("w-full")
                password = ui.input(
                    "Contraseña", value=os.getenv("NEO4J_PASSWORD", ""),
                    password=True, password_toggle_button=True,
                ).classes("w-full")
                database = ui.input(
                    "Base de datos (opcional)", value=os.getenv("NEO4J_DATABASE", ""),
                    placeholder="Por defecto del servidor",
                ).classes("w-full")
                error = ui.label().classes("text-negative text-caption")
                error.set_visibility(False)

                def on_mode() -> None:
                    uri.set_value(LOCAL_URI if mode.value == "local" else AURA_URI)
                    hint.set_text(HINTS[mode.value])

                mode.on_value_change(on_mode)

                async def connect() -> None:
                    error.set_visibility(False)
                    if not uri.value.strip() or not user.value.strip():
                        ui.notify("URI y usuario son obligatorios.", type="warning")
                        return
                    connect_btn.props("loading")
                    try:
                        await run.io_bound(
                            service.connect, uri.value.strip(), user.value.strip(),
                            password.value, database.value.strip() or None,
                        )
                    except Exception as e:  # noqa: BLE001 - se muestra al usuario
                        error.set_text(f"No se pudo conectar: {e}")
                        error.set_visibility(True)
                        return
                    finally:
                        connect_btn.props(remove="loading")
                    ui.navigate.to("/app")

                for field in (uri, user, password, database):
                    field.on("keydown.enter", connect)

                connect_btn = ui.button("Conectar", icon="power", on_click=connect).classes("w-full")
