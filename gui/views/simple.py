"""Vista CRUD genérica para las entidades simples (User, Tag, Category)."""
from __future__ import annotations

from nicegui import ui

from db import Neo4jService
from gui.views.common import Refresh, call, col, confirm, crud_table, form_dialog


def simple_view(service: Neo4jService, label: str, singular: str, fields: list[tuple[str, str]],
                delete_warning: str = "") -> Refresh:
    """Construye la tabla CRUD de un nodo simple y devuelve su función `refresh`."""

    async def refresh() -> None:
        if not service.connected:
            table.rows = []
            table.update()
            return
        rows = await call(service, service.list_nodes, label)
        if rows is not None:
            table.rows = rows
            table.update()

    async def open_form(row: dict | None = None) -> None:
        values = row or {}

        def build() -> dict[str, ui.element]:
            return {k: ui.input(lbl, value=values.get(k, "")).classes("w-full") for k, lbl in fields}

        data = await form_dialog(f"{'Editar' if row else 'Nuevo'} {singular}", build)
        if data is None:
            return
        if row:
            ok = await call(service, service.update_node, label, row["id"], data)
        else:
            ok = await call(service, service.create_node, label, data)
        if ok:
            ui.notify("Guardado.", type="positive")
            await refresh()

    async def delete(row: dict) -> None:
        if not await confirm(f"¿Eliminar {singular} '{row['name']}'? {delete_warning}".strip()):
            return
        if await call(service, service.delete_node, label, row["id"]):
            ui.notify("Eliminado.", type="positive")
            await refresh()

    table = crud_table(
        [col(k, lbl) for k, lbl in fields],
        on_add=open_form, on_edit=open_form, on_delete=delete, add_label=f"Nuevo {singular}",
    )
    return refresh
