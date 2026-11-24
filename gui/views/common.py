"""Utilidades de interfaz compartidas por las vistas."""
from __future__ import annotations

import re
from typing import Any, Awaitable, Callable

from nicegui import run, ui

from db import Neo4jService

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

ACTIONS_SLOT = """
<q-td :props="props">
  <q-btn flat dense round color="primary" icon="edit" @click="() => $parent.$emit('edit', props.row)" />
  <q-btn flat dense round color="negative" icon="delete" @click="() => $parent.$emit('delete', props.row)" />
</q-td>
"""
ACTIONS_COLUMN = {"name": "actions", "label": "", "field": "actions", "align": "right"}
ELLIPSIS = "max-width: 280px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap"

Refresh = Callable[[], Awaitable[None]]
"""Corrutina que recarga los datos de una vista."""


async def call(service: Neo4jService, fn: Callable[..., Any], *args: Any) -> Any:
    """Ejecuta una llamada bloqueante a la BD en un hilo. Devuelve None si falla."""
    if not service.connected:
        ui.notify("No hay conexión con la base de datos.", type="negative")
        return None
    try:
        return await run.io_bound(fn, *args)
    except Exception as e:  # noqa: BLE001 - se muestra al usuario
        ui.notify(f"Error: {e}", type="negative", multi_line=True)
        return None


async def confirm(message: str) -> bool:
    with ui.dialog() as dialog, ui.card():
        ui.label(message)
        with ui.row().classes("w-full justify-end"):
            ui.button("Cancelar", on_click=lambda: dialog.submit(False)).props("flat")
            # [TEMA] "negative" = rojo de la paleta (theme/colors.py).
            ui.button("Eliminar", color="negative", on_click=lambda: dialog.submit(True))
    result = await dialog
    dialog.delete()
    return bool(result)


async def form_dialog(
    title: str,
    build: Callable[[], dict[str, ui.element]],
    optional: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    """Muestra un formulario modal. `build` crea los campos y devuelve {clave: elemento}."""
    with ui.dialog() as dialog, ui.card().classes("w-[32rem] max-w-full"):
        # [TEMA] `app-dialog-title`: título en color primary (theme/styles.py).
        ui.label(title).classes("text-h6 app-dialog-title")
        fields = build()

        def save() -> None:
            data = {k: (el.value.strip() if isinstance(el.value, str) else el.value)
                    for k, el in fields.items()}
            if any(k not in optional and v in (None, "") for k, v in data.items()):
                ui.notify("Completa todos los campos obligatorios.", type="warning")
                return
            if "email" in data and not EMAIL_RE.match(data["email"]):
                ui.notify("El email no es válido.", type="warning")
                return
            dialog.submit(data)

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancelar", on_click=dialog.close).props("flat")
            ui.button("Guardar", on_click=save)
    result = await dialog
    dialog.delete()
    return result


def crud_table(
    columns: list[dict[str, Any]],
    on_add: Callable[[], Awaitable[None]],
    on_edit: Callable[[dict], Awaitable[None]],
    on_delete: Callable[[dict], Awaitable[None]],
    add_label: str,
    on_details: Callable[[dict], Awaitable[None]] | None = None,
    details_tooltip: str = "Ver detalles",
) -> ui.table:
    """Tabla con búsqueda y acciones por fila. Si se pasa `on_details` añade un botón "ver"."""
    with ui.row().classes("w-full items-center"):
        search = ui.input("Buscar").props("dense outlined clearable").classes("w-64")
        ui.space()
        ui.button(add_label, icon="add", on_click=on_add)
    # [TEMA] `app-table`: cabecera, bordes y hover de la tabla (theme/styles.py).
    table = ui.table(columns=[*columns, ACTIONS_COLUMN], rows=[], row_key="id").classes("w-full app-table")
    search.bind_value_to(table, "filter")
    if on_details is not None:
        details_btn = (
            '<q-btn flat dense round color="secondary" icon="visibility" '
            "@click=\"() => $parent.$emit('details', props.row)\">"
            f"<q-tooltip>{details_tooltip}</q-tooltip></q-btn>"
        )
        table.add_slot("body-cell-actions", ACTIONS_SLOT.replace("<q-td :props=\"props\">",
                                                                 "<q-td :props=\"props\">\n  " + details_btn))
        table.on("details", lambda e: on_details(e.args))
    else:
        table.add_slot("body-cell-actions", ACTIONS_SLOT)
    table.on("edit", lambda e: on_edit(e.args))
    table.on("delete", lambda e: on_delete(e.args))
    return table


def col(name: str, label: str, ellipsis: bool = False) -> dict[str, Any]:
    column: dict[str, Any] = {"name": name, "label": label, "field": name, "align": "left", "sortable": True}
    if ellipsis:
        column["style"] = ELLIPSIS
        column["headerStyle"] = ""
    return column


def options(rows: list[dict], label_key: str) -> dict[str, str]:
    return {r["id"]: r[label_key] for r in rows}
