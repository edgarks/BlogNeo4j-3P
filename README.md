# Blog Neo4j + NiceGUI

CRUD de usuarios, artículos, tags, categorías y comentarios sobre Neo4j (Cypher).
Al iniciar aparece un formulario de conexión (base local o Neo4j Aura). Cuando la
conexión se verifica, se abre el dashboard con una vista por entidad. Sin conexión
no se puede acceder a `/app`; el botón **Desconectar** vuelve al formulario.

## Ejecutar la aplicación

```bash
pip install -r requirements.txt
python main.py
```

Abre http://localhost:8080.

- **Local**: `bolt://localhost:7687`, usuario `neo4j` y la contraseña de tu instancia.
- **Aura**: URI `neo4j+s://<id>.databases.neo4j.io`, usuario y contraseña del fichero de credenciales de Aura.

Opcionalmente se pueden prerrellenar los campos con las variables de entorno
`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` y `NEO4J_DATABASE`.

## Estructura del proyecto

```
│   db.py  --->  Acceso a Neo4j (Cypher)
│   main.py  --->  Punto de entrada
│   README.md
│
├───.nicegui
│       storage-general.json
│
├───gui
│   │   dashboard.py  --->  "/app" ventana principal con pestañas (requiere conexión)
│   │   login.py  --->  "/" Formulario de conexión
│   │   pages.py  --->  Registra las páginas
│   │   __init__.py
│   │
│   ├───views
│       │   articles.py
│       │   categories.py
│       │   comments.py
│       │   common.py  --->  Helpers de UI (tabla, diálogos, etc.)
│       │   registry.py  --->  Lista de vistas del dashboard
│       │   simple.py  --->  CRUD genérico para User/Tag/Category
│       │   tags.py
│       │   users.py
│       │   __init__.py
│
├───theme
│   │   colors.py  --->  paletas de colores: Colores de marca (Quasar) y claro/oscuro
│   │   core.py  --->  Funciones "apply_theme()" y "theme_toggle() (modo oscuro)
│   │   icon.py  --->  Ícono de ventana nativa / favicon
│   │   make_icon.py  --->  Genera icon.ico/png (opcional, requiere Pillow)
│   │   settings.py  --->  Configuración de nombre, ícono, material, tamaño de ventana, fuente y radio
│   │   styles.py  --->  CSS global generado desde la paleta
│   │   __init__.py
│   │
│   ├───assets
│           icon.ico
│           icon.png
│           icon.svg


```

## Temas e íconos

Todo lo visual vive en `theme/`. Cada página llama a `apply_theme()` al empezar.
Para cambiar colores edita `theme/colors.py`; el modo oscuro se alterna con el
botón de la cabecera y se recuerda entre ejecuciones.

Ícono: coloca tu `icon.ico` (Windows), `icon.png` (Linux) o `icon.icns` (macOS)
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

Nota: Al borrar un usuario se borran sus artículos y comentarios; al borrar un artículo,
sus comentarios. Borrar un tag o una categoría solo elimina la relación.
