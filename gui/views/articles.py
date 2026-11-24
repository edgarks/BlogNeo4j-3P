"""Vista de artículos."""
from __future__ import annotations

from datetime import date

from nicegui import ui

from db import Neo4jService
from gui.views.common import Refresh, call, col, confirm, crud_table, form_dialog, options


def build(service: Neo4jService) -> Refresh:
    async def refresh() -> None:
        if not service.connected:
            table.rows = []
            table.update()
            return
        rows = await call(service, service.list_articles)
        if rows is not None:
            for r in rows:
                r["tags_text"] = ", ".join(r["tag_names"])
                r["categories_text"] = ", ".join(r["category_names"])
            table.rows = rows
            table.update()

    async def open_form(row: dict | None = None) -> None:
        users = await call(service, service.list_nodes, "User")
        tags = await call(service, service.list_nodes, "Tag")
        categories = await call(service, service.list_nodes, "Category")
        if users is None or tags is None or categories is None:
            return
        if not users:
            ui.notify("Crea al menos un usuario antes de escribir un artículo.", type="warning")
            return
        v = row or {}

        def build() -> dict[str, ui.element]:
            return {
                "title": ui.input("Título", value=v.get("title", "")).classes("w-full"),
                "user_id": ui.select(options(users, "name"), label="Autor",
                                     value=v.get("user_id")).classes("w-full"),
                "date": ui.input("Fecha", value=v.get("date") or date.today().isoformat())
                .props("type=date stack-label").classes("w-full"),
                "text": ui.textarea("Texto", value=v.get("text", "")).classes("w-full"),
                "tag_ids": ui.select(options(tags, "name"), label="Tags", multiple=True,
                                     value=v.get("tag_ids", [])).props("use-chips").classes("w-full"),
                "category_ids": ui.select(options(categories, "name"), label="Categorías", multiple=True,
                                          value=v.get("category_ids", [])).props("use-chips")
                .classes("w-full"),
            }

        data = await form_dialog(f"{'Editar' if row else 'Nuevo'} artículo", build,
                                 optional=("tag_ids", "category_ids"))
        if data is None:
            return
        if row:
            ok = await call(service, service.update_article, row["id"], data)
        else:
            ok = await call(service, service.create_article, data)
        if ok:
            ui.notify("Guardado.", type="positive")
            await refresh()

    async def delete(row: dict) -> None:
        if not await confirm(f"¿Eliminar el artículo '{row['title']}' y sus comentarios?"):
            return
        if await call(service, service.delete_article, row["id"]):
            ui.notify("Eliminado.", type="positive")
            await refresh()

    async def show_details(row: dict) -> None:
        details = await call(service, service.get_article_details, row["id"])
        if details is None:
            return

        def section(title: str, icon: str, items: list[dict], show_user: bool = False) -> None:
            ui.label(f"{title} ({len(items)})").classes("text-subtitle1 text-bold mt-2")
            if not items:
                # [TEMA] `app-muted` sustituye a `text-grey` (se adapta al modo oscuro).
                ui.label("Sin elementos.").classes("app-muted")
                return
            with ui.list().props("dense separator").classes("w-full"):
                for item in items:
                    with ui.item():
                        with ui.item_section().props("avatar"):
                            ui.icon(icon, color="primary")
                        with ui.item_section():
                            ui.item_label(item.get("name") or "(sin nombre)")
                            if show_user and item.get("user"):
                                ui.item_label(f"por {item['user']}").props("caption")
                            if item.get("url"):
                                ui.link(item["url"], item["url"], new_tab=True).classes("text-caption")

        with ui.dialog() as dialog, ui.card().classes("w-[32rem] max-w-full"):
            with ui.row().classes("w-full items-center no-wrap"):
                ui.label(row["title"]).classes("text-h6 ellipsis app-dialog-title")
                ui.space()
                ui.button(icon="close", on_click=dialog.close).props("flat round dense")
            with ui.scroll_area().classes("w-full h-96"):
                section("Comentarios", "comment", details["comments"], show_user=True)
                section("Categorías", "category", details["categories"])
                section("Tags", "sell", details["tags"])
            with ui.row().classes("w-full justify-end"):
                ui.button("Cerrar", on_click=dialog.close).props("flat")
        dialog.on("hide", dialog.delete)
        dialog.open()

    table = crud_table(
        [col("title", "Título"), col("user_name", "Autor"), col("date", "Fecha"),
         col("text", "Texto", ellipsis=True), col("tags_text", "Tags"),
         col("categories_text", "Categorías"), col("comments", "Comentarios")],
        on_add=open_form, on_edit=open_form, on_delete=delete, add_label="Nuevo artículo",
        on_details=show_details, details_tooltip="Ver comentarios, categorías y tags",
    )
    return refresh
