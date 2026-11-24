"""Vista de usuarios."""
from __future__ import annotations

from db import Neo4jService
from gui.views.common import Refresh
from gui.views.simple import simple_view


def build(service: Neo4jService) -> Refresh:
    return simple_view(
        service, "User", "usuario", [("name", "Nombre"), ("email", "Email")],
        delete_warning="Se eliminarán también sus artículos y comentarios.",
    )
