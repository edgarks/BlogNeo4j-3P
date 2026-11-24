# Blog Neo4j + NiceGUI

CRUD de usuarios, artículos, tags, categorías y comentarios sobre Neo4j (Cypher).
Al iniciar aparece un formulario de conexión (base local o Neo4j Aura). Cuando la
conexión se verifica, se abre el dashboard con una vista por entidad. Sin conexión
no se puede acceder a `/app`; el botón **Desconectar** vuelve al formulario.

## Ejecutar

```bash
pip install -r requirements.txt
python main.py
```

Abre http://localhost:8080.

- **Local**: `bolt://localhost:7687`, usuario `neo4j` y la contraseña de tu instancia.
- **Aura**: URI `neo4j+s://<id>.databases.neo4j.io`, usuario y contraseña del fichero de credenciales de Aura.

Opcionalmente se pueden prerellenar los campos con las variables de entorno
`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` y `NEO4J_DATABASE`.

## Estructura

```
main.py                 punto de entrada
db.py                   acceso a Neo4j (Cypher)
theme/
  settings.py           nombre, icono Material, tamaño de ventana, fuente, radio
  colors.py             paletas: colores de marca (Quasar) y claro/oscuro
  styles.py             CSS global generado desde la paleta
  core.py               apply_theme() y theme_toggle() (modo oscuro)
  icon.py               icono de ventana nativa / favicon
  make_icon.py          genera icon.ico/png (opcional, requiere Pillow)
  assets/               icon.svg, icon.ico, icon.png
gui/
  pages.py              registra las páginas
  login.py              "/"    formulario de conexión
  dashboard.py          "/app" ventana principal con pestañas (requiere conexión)
  views/
    registry.py         lista de vistas del dashboard
    common.py           helpers de UI (tabla, diálogos, ...)
    simple.py           CRUD genérico para User/Tag/Category
    users.py  articles.py  tags.py  categories.py  comments.py
```

## Tema e icono

Todo lo visual vive en `theme/`. Cada página llama a `apply_theme()` al empezar.
Para cambiar colores edita `theme/colors.py`; el modo oscuro se alterna con el
botón de la cabecera y se recuerda entre ejecuciones.

Icono: coloca tu `icon.ico` (Windows), `icon.png` (Linux) o `icon.icns` (macOS)
en `theme/assets/`. Si no tienes uno: `pip install pillow` y
`python -m theme.make_icon` genera uno por defecto.

Para añadir una vista: crea un módulo en `gui/views/` con `build(service) -> refresh`
y regístralo en `registry.py`.

## Modelo de grafo

| Relación | Significado |
|---|---|
| `(:User)-[:WROTE]->(:Article)` | 1 usuario : N artículos |
| `(:Article)-[:HAS_TAG]->(:Tag)` | N artículos : N tags |
| `(:Article)-[:IN_CATEGORY]->(:Category)` | N artículos : N categorías |
| `(:Article)-[:HAS_COMMENT]->(:Comment)` | 1 artículo : N comentarios |
| `(:User)-[:POSTED]->(:Comment)` | 1 usuario : N comentarios |

Propiedades: `User{name,email}`, `Article{title,date,text}`, `Tag{name,url}`,
`Category{name,url}`, `Comment{name,url}`. Cada nodo tiene además un `id` (UUID) único.

Al borrar un usuario se borran sus artículos y comentarios; al borrar un artículo,
sus comentarios. Borrar un tag o una categoría solo elimina la relación.
