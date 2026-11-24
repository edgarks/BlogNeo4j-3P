"""CSS global de la aplicación, generado a partir de `colors` y `settings`.

Clases propias que usan las vistas:

    app-header        cabecera del dashboard (degradado)
    app-tabs          barra de pestañas del dashboard
    app-table         tablas CRUD
    app-muted         texto secundario
    app-dialog-title  título de diálogos/formularios
    app-login-bg      fondo degradado de la pantalla de login (se pone en <body>)
    app-login-card    tarjeta del formulario de login

Además se sobreescriben componentes de Quasar (`.q-card`, `.q-menu`) para que
respeten la paleta en modo claro y oscuro.
"""
from __future__ import annotations

from theme.colors import DARK, LIGHT
from theme.settings import FONT_FAMILY, RADIUS


def build_css() -> str:
    return f"""
/* ---- Variables ------------------------------------------------------ */
:root {{
  --app-radius: {RADIUS};
  --app-font: {FONT_FAMILY};
}}
/* Quasar añade `body--light` / `body--dark` según el modo activo. */
body.body--light {{
{LIGHT.css_variables()}
}}
body.body--dark {{
{DARK.css_variables()}
}}

/* ---- Base ----------------------------------------------------------- */
body.body--light, body.body--dark {{
  background: var(--app-background) !important;
  color: var(--app-text);
}}
body, .q-btn, .q-tab, .q-field, .q-table, .q-item {{
  font-family: var(--app-font);
}}
.app-muted {{ color: var(--app-text-muted); }}

/* ---- Cabecera ------------------------------------------------------- */
.q-header.app-header {{
  background: linear-gradient(90deg, var(--app-header-from), var(--app-header-to)) !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.25);
}}

/* ---- Pestañas y paneles --------------------------------------------- */
.app-tabs {{
  background: var(--app-surface);
  color: var(--app-text-muted);
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius);
}}
.q-tab-panels, .q-tab-panel {{ background: transparent !important; color: var(--app-text); }}

/* ---- Tarjetas, diálogos y menús ------------------------------------- */
.q-card {{
  background: var(--app-surface);
  color: var(--app-text);
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius);
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
}}
.q-menu {{
  background: var(--app-surface);
  color: var(--app-text);
  border: 1px solid var(--app-border);
}}
.app-dialog-title {{ color: var(--q-primary); font-weight: 600; }}

/* ---- Tablas --------------------------------------------------------- */
.app-table {{
  background: var(--app-surface) !important;
  color: var(--app-text) !important;
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius);
  box-shadow: none !important;
}}
.app-table th, .app-table td, .app-table .q-table__bottom {{
  border-color: var(--app-border) !important;
}}
.app-table thead th {{
  background: var(--app-table-header);
  color: var(--app-text-muted);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
}}
.app-table tbody tr:hover td {{ background: var(--app-row-hover); }}

/* ---- Login ---------------------------------------------------------- */
body.body--light.app-login-bg, body.body--dark.app-login-bg {{
  background: linear-gradient(135deg, var(--app-login-from), var(--app-login-to)) fixed !important;
}}
.app-login-card {{ box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18); }}
"""
