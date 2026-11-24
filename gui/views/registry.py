"""Listado de vistas disponibles en el dashboard.

Para añadir una vista nueva: crea un módulo en `gui/views/` con una función
`build(service) -> Refresh` y regístralo aquí.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from db import Neo4jService
from gui.views import articles, categories, comments, tags, users
from gui.views.common import Refresh


@dataclass(frozen=True)
class View:
    key: str
    title: str
    icon: str
    build: Callable[[Neo4jService], Refresh]


VIEWS: tuple[View, ...] = (
    View("users", "Usuarios", "person", users.build),
    View("articles", "Artículos", "article", articles.build),
    View("tags", "Tags", "sell", tags.build),
    View("categories", "Categorías", "category", categories.build),
    View("comments", "Comentarios", "comment", comments.build),
)
