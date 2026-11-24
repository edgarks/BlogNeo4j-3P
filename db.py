"""Acceso a Neo4j (Cypher) para el modelo blog.

Modelo de grafo:

    (:User {id, name, email})
        -[:WROTE]->  (:Article {id, title, date, text})
        -[:POSTED]-> (:Comment {id, name, url})
    (:Article)-[:HAS_TAG]->      (:Tag {id, name, url})
    (:Article)-[:IN_CATEGORY]->  (:Category {id, name, url})
    (:Article)-[:HAS_COMMENT]->  (:Comment)

Todos los nodos tienen una propiedad `id` (UUID) usada como clave de negocio.
"""
from __future__ import annotations

import uuid
from contextlib import contextmanager
from typing import Any, Iterable, Iterator

"""Importar el driver y sus utilidades"""
from neo4j import Driver, GraphDatabase, Session

# Entidades "simples" (sin relaciones editables): label -> campos
SIMPLE_ENTITIES: dict[str, tuple[str, ...]] = {
    "User": ("name", "email"),
    "Tag": ("name", "url"),
    "Category": ("name", "url"),
}

Statement = tuple[str, dict[str, Any]]

"""Función para generar UUID aleatorias"""
def _new_id() -> str:
    return str(uuid.uuid4())


class _Executor:
    """Ejecuta consultas Cypher sobre una sesión abierta del driver."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def read(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        def work(tx):
            return [record.data() for record in tx.run(query, params or {})]

        return self._session.execute_read(work)

    def write(self, statements: Iterable[Statement]) -> bool:
        """Ejecuta varias sentencias Cypher en una única transacción."""
        statements = list(statements)

        def work(tx):
            for query, params in statements:
                tx.run(query, params).consume()

        self._session.execute_write(work)
        return True


class Neo4jService:
    def __init__(self) -> None:
        self.driver: Driver | None = None
        self.database: str | None = None
        self.uri: str = ""

    # ------------------------------------------------------------------
    # Conexión
    # ------------------------------------------------------------------
    """Regresa si esta conectado o no"""
    @property
    def connected(self) -> bool:
        return self.driver is not None
    """Realiza la conexión a la base de datos"""
    def connect(self, uri: str, user: str, password: str, database: str | None = None) -> None:
        self.close()
        driver = GraphDatabase.driver(uri, auth=(user, password))
        try:
            driver.verify_connectivity()
        except Exception:
            driver.close()
            raise
        self.driver = driver
        self.database = database or None
        self.uri = uri
        self._ensure_constraints()
    """Termina la conexión y reinicia el driver (para que no quede en cache los datos)"""
    def close(self) -> None:
        if self.driver is not None:
            self.driver.close()
        self.driver = None
        self.uri = ""
    """Se asegura que los modelos existentes cumplan con los requisitos del diagrama"""
    def _ensure_constraints(self) -> None:
        with self._session() as db:
            for label in ("User", "Article", "Tag", "Category", "Comment"):
                try:
                    db.write([(
                        f"CREATE CONSTRAINT {label.lower()}_id IF NOT EXISTS "
                        f"FOR (n:{label}) REQUIRE n.id IS UNIQUE", {})])
                except Exception:
                    # Versiones antiguas de Neo4j usan otra sintaxis; no es crítico.
                    pass

    # ------------------------------------------------------------------
    # Ejecución
    # ------------------------------------------------------------------
    @contextmanager
    def _session(self) -> Iterator[_Executor]:
        """Abre una sesión del driver y entrega un ejecutor (`read`/`write`) ligado a ella."""
        if self.driver is None:
            raise RuntimeError("No hay conexión con la base de datos.")
        with self.driver.session(database=self.database) as session:
            yield _Executor(session)

    # ------------------------------------------------------------------
    # CRUD genérico: User, Tag, Category
    # ------------------------------------------------------------------
    @staticmethod
    def _fields(label: str) -> tuple[str, ...]:
        try:
            return SIMPLE_ENTITIES[label]
        except KeyError:
            raise ValueError(f"Entidad no soportada: {label}") from None

    def list_nodes(self, label: str) -> list[dict[str, Any]]:
        fields = self._fields(label)  # valida el label (se interpola en la query)
        returned = ", ".join(f"n.{f} AS {f}" for f in fields)
        with self._session() as db:
            return db.read(f"MATCH (n:{label}) RETURN n.id AS id, {returned} ORDER BY toLower(n.name)")

    def create_node(self, label: str, data: dict[str, Any]) -> bool:
        fields = self._fields(label)
        props = {f: data[f] for f in fields}
        with self._session() as db:
            return db.write([(f"CREATE (n:{label} {{id: $id}}) SET n += $props",
                              {"id": _new_id(), "props": props})])

    def update_node(self, label: str, node_id: str, data: dict[str, Any]) -> bool:
        fields = self._fields(label)
        props = {f: data[f] for f in fields}
        with self._session() as db:
            return db.write([(f"MATCH (n:{label} {{id: $id}}) SET n += $props",
                              {"id": node_id, "props": props})])

    def delete_node(self, label: str, node_id: str) -> bool:
        self._fields(label)
        p = {"id": node_id}
        with self._session() as db:
            if label == "User":
                # Borrado en cascada: comentarios en sus artículos, sus comentarios y sus artículos.
                return db.write([
                    ("MATCH (:User {id: $id})-[:WROTE]->(:Article)-[:HAS_COMMENT]->(c:Comment) DETACH DELETE c", p),
                    ("MATCH (:User {id: $id})-[:POSTED]->(c:Comment) DETACH DELETE c", p),
                    ("MATCH (:User {id: $id})-[:WROTE]->(a:Article) DETACH DELETE a", p),
                    ("MATCH (u:User {id: $id}) DETACH DELETE u", p),
                ])
            return db.write([(f"MATCH (n:{label} {{id: $id}}) DETACH DELETE n", p)])

    # ------------------------------------------------------------------
    # Artículos
    # ------------------------------------------------------------------
    def list_articles(self) -> list[dict[str, Any]]:
        with self._session() as db:
            return db.read("""
                MATCH (a:Article)
                OPTIONAL MATCH (u:User)-[:WROTE]->(a)
                OPTIONAL MATCH (a)-[:HAS_TAG]->(t:Tag)
                OPTIONAL MATCH (a)-[:IN_CATEGORY]->(c:Category)
                OPTIONAL MATCH (a)-[:HAS_COMMENT]->(cm:Comment)
                RETURN a.id AS id, a.title AS title, toString(a.date) AS date, a.text AS text,
                       u.id AS user_id, u.name AS user_name,
                       collect(DISTINCT t.id) AS tag_ids, collect(DISTINCT t.name) AS tag_names,
                       collect(DISTINCT c.id) AS category_ids, collect(DISTINCT c.name) AS category_names,
                       count(DISTINCT cm) AS comments
                ORDER BY date DESC, toLower(title)
            """)

    def get_article_details(self, article_id: str) -> dict[str, Any]:
        """Tags, categorías y comentarios (con su autor) de un artículo."""
        with self._session() as db:
            rows = db.read("""
                MATCH (a:Article {id: $id})
                RETURN a.title AS title,
                       [(a)-[:HAS_TAG]->(t:Tag) | {name: t.name, url: t.url}] AS tags,
                       [(a)-[:IN_CATEGORY]->(c:Category) | {name: c.name, url: c.url}] AS categories,
                       [(a)-[:HAS_COMMENT]->(cm:Comment) |
                           {name: cm.name, url: cm.url, user: head([(u:User)-[:POSTED]->(cm) | u.name])}
                       ] AS comments
            """, {"id": article_id})
        if not rows:
            return {"title": "", "tags": [], "categories": [], "comments": []}
        details = rows[0]
        for key in ("tags", "categories", "comments"):
            details[key].sort(key=lambda item: (item.get("name") or "").lower())
        return details

    @staticmethod
    def _link_statements(article_id: str, tag_ids: list[str], category_ids: list[str]) -> list[Statement]:
        p = {"id": article_id, "tag_ids": tag_ids, "category_ids": category_ids}
        return [
            ("MATCH (a:Article {id: $id}) MATCH (t:Tag) WHERE t.id IN $tag_ids "
             "MERGE (a)-[:HAS_TAG]->(t)", p),
            ("MATCH (a:Article {id: $id}) MATCH (c:Category) WHERE c.id IN $category_ids "
             "MERGE (a)-[:IN_CATEGORY]->(c)", p),
        ]

    def create_article(self, data: dict[str, Any]) -> bool:
        article_id = _new_id()
        with self._session() as db:
            return db.write([
                ("MATCH (u:User {id: $user_id}) "
                 "CREATE (u)-[:WROTE]->(:Article {id: $id, title: $title, date: date($date), text: $text})",
                 {"id": article_id, "user_id": data["user_id"], "title": data["title"],
                  "date": data["date"], "text": data["text"]}),
                *self._link_statements(article_id, data.get("tag_ids") or [], data.get("category_ids") or []),
            ])

    def update_article(self, article_id: str, data: dict[str, Any]) -> bool:
        p = {"id": article_id, "user_id": data["user_id"], "title": data["title"],
             "date": data["date"], "text": data["text"]}
        with self._session() as db:
            return db.write([
                ("MATCH (a:Article {id: $id}) SET a.title = $title, a.date = date($date), a.text = $text", p),
                ("MATCH (:User)-[w:WROTE]->(:Article {id: $id}) DELETE w", p),
                ("MATCH (u:User {id: $user_id}), (a:Article {id: $id}) MERGE (u)-[:WROTE]->(a)", p),
                ("MATCH (:Article {id: $id})-[r:HAS_TAG|IN_CATEGORY]->() DELETE r", p),
                *self._link_statements(article_id, data.get("tag_ids") or [], data.get("category_ids") or []),
            ])

    def delete_article(self, article_id: str) -> bool:
        p = {"id": article_id}
        with self._session() as db:
            return db.write([
                ("MATCH (:Article {id: $id})-[:HAS_COMMENT]->(c:Comment) DETACH DELETE c", p),
                ("MATCH (a:Article {id: $id}) DETACH DELETE a", p),
            ])

    # ------------------------------------------------------------------
    # Comentarios
    # ------------------------------------------------------------------
    def list_comments(self) -> list[dict[str, Any]]:
        with self._session() as db:
            return db.read("""
                MATCH (c:Comment)
                OPTIONAL MATCH (u:User)-[:POSTED]->(c)
                OPTIONAL MATCH (a:Article)-[:HAS_COMMENT]->(c)
                RETURN c.id AS id, c.name AS name, c.url AS url,
                       u.id AS user_id, u.name AS user_name,
                       a.id AS article_id, a.title AS article_title
                ORDER BY toLower(c.name)
            """)

    def create_comment(self, data: dict[str, Any]) -> bool:
        with self._session() as db:
            return db.write([(
                "MATCH (u:User {id: $user_id}), (a:Article {id: $article_id}) "
                "CREATE (u)-[:POSTED]->(c:Comment {id: $id, name: $name, url: $url}), "
                "(a)-[:HAS_COMMENT]->(c)",
                {"id": _new_id(), **{k: data[k] for k in ("user_id", "article_id", "name", "url")}},
            )])

    def update_comment(self, comment_id: str, data: dict[str, Any]) -> bool:
        p = {"id": comment_id, **{k: data[k] for k in ("user_id", "article_id", "name", "url")}}
        with self._session() as db:
            return db.write([
                ("MATCH (c:Comment {id: $id}) SET c.name = $name, c.url = $url", p),
                ("MATCH (:User)-[r:POSTED]->(:Comment {id: $id}) DELETE r", p),
                ("MATCH (:Article)-[r:HAS_COMMENT]->(:Comment {id: $id}) DELETE r", p),
                ("MATCH (c:Comment {id: $id}), (u:User {id: $user_id}), (a:Article {id: $article_id}) "
                 "CREATE (u)-[:POSTED]->(c), (a)-[:HAS_COMMENT]->(c)", p),
            ])

    def delete_comment(self, comment_id: str) -> bool:
        with self._session() as db:
            return db.write([("MATCH (c:Comment {id: $id}) DETACH DELETE c", {"id": comment_id})])
