"""Vista de comentarios."""
from __future__ import annotations

from nicegui import ui

from db import Neo4jService
from gui.views.common import Refresh, call, col, confirm, crud_table, form_dialog, options


def build(service: Neo4jService) -> Refresh:
    async def refresh() -> None:
        if not service.connected:
            table.rows = []
            table.update()
            return
        rows = await call(service, service.list_comments)
        if rows is not None:
            table.rows = rows
            table.update()

    async def open_form(row: dict | None = None) -> None:
        users = await call(service, service.list_nodes, "User")
        articles = await call(service, service.list_articles)
        if users is None or articles is None:
            return
        if not users or not articles:
            ui.notify("Necesitas al menos un usuario y un artículo.", type="warning")
            return
        v = row or {}

        def build() -> dict[str, ui.element]:
            return {
                "name": ui.input("Nombre", value=v.get("name", "")).classes("w-full"),
                "url": ui.input("URL", value=v.get("url", "")).classes("w-full"),
                "user_id": ui.select(options(users, "name"), label="Usuario",
                                     value=v.get("user_id")).classes("w-full"),
                "article_id": ui.select(options(articles, "title"), label="Artículo",
                                        value=v.get("article_id")).classes("w-full"),
            }

        data = await form_dialog(f"{'Editar' if row else 'Nuevo'} comentario", build)
        if data is None:
            return
        if row:
            ok = await call(service, service.update_comment, row["id"], data)
        else:
            ok = await call(service, service.create_comment, data)
        if ok:
            ui.notify("Guardado.", type="positive")
            await refresh()

    async def delete(row: dict) -> None:
        if not await confirm(f"¿Eliminar el comentario '{row['name']}'?"):
            return
        if await call(service, service.delete_comment, row["id"]):
            ui.notify("Eliminado.", type="positive")
            await refresh()

    table = crud_table(
        [col("name", "Nombre"), col("url", "URL"), col("user_name", "Usuario"),
         col("article_title", "Artículo")],
        on_add=open_form, on_edit=open_form, on_delete=delete, add_label="Nuevo comentario",
    )
    return refresh
