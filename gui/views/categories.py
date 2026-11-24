"""Vista de categorías."""
from __future__ import annotations

from db import Neo4jService
from gui.views.common import Refresh
from gui.views.simple import simple_view


def build(service: Neo4jService) -> Refresh:
    return simple_view(service, "Category", "categoría", [("name", "Nombre"), ("url", "URL")])
