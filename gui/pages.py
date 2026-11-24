"""Registro de las páginas de la aplicación."""
from __future__ import annotations

from db import Neo4jService
from gui import dashboard, login


def register_pages(service: Neo4jService) -> None:
    """`/` -> formulario de conexión; `/app` -> dashboard (solo con conexión activa)."""
    login.register(service)
    dashboard.register(service)
