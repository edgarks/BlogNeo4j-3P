"""Seed de datos de ejemplo para el blog (Neo4j).

Crea 5 usuarios, 3 categorías, tags, 13 artículos (2-3 por usuario) y comentarios:
en cada artículo comentan 2 usuarios elegidos al azar entre los demás (nunca el autor).

Es idempotente: usa ids deterministas y MERGE, así que se puede ejecutar varias veces
sin duplicar datos (con el mismo --seed).

Uso:
    python seed.py                 # usa NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD / NEO4J_DATABASE
    python seed.py --reset         # borra antes todos los datos del blog
    python seed.py --seed 7        # otra combinación aleatoria de comentaristas
"""
from __future__ import annotations

import argparse
import os
import random
from getpass import getpass

from db import Neo4jService

BASE_URL = "https://blog.uach.mx"

USERS = ["Neko", "Edgar", "Alan", "Jesus", "Amir"]

CATEGORIES = {
    "programacion": "Programación",
    "videojuegos": "Videojuegos",
    "terror-cosmico": "Libros de terror cósmico",
}

TAGS = [
    "Neo4j", "Bases de datos", "Grafos", "Python", "Tipado", "Buenas prácticas", "Rust", "Memoria",
    "Algoritmos", "Complejidad", "Refactorización", "Metroidvania", "Indie", "Diseño de niveles",
    "RPG", "Soulslike", "Mundo abierto", "Narrativa", "Roguelike", "Lovecraft", "Cthulhu",
    "Horror cósmico", "Antártida", "Cuento",
]

# autor, categorías, tags, fecha, título, texto, [comentarios (2)]
ARTICLES = [
    ("Neko", ["programacion"], ["Neo4j", "Bases de datos", "Grafos"], "2026-09-02",
     "Por qué los grafos modelan mejor las relaciones",
     "Cuando los datos están muy conectados, como usuarios, artículos y comentarios, una base de "
     "grafos evita los JOIN encadenados. En Neo4j las relaciones son ciudadanos de primera clase "
     "y se recorren con Cypher de forma natural.",
     ["Justo lo que necesitaba para el proyecto de la clase, gracias por la comparación.",
      "Los JOIN de cinco tablas me dieron pesadillas; Cypher se lee mucho mejor."]),
    ("Neko", ["videojuegos"], ["Metroidvania", "Indie", "Diseño de niveles"], "2026-09-15",
     "Hollow Knight: diseño de un mundo interconectado",
     "Hallownest funciona porque cada atajo y cada puerta bloqueada te invita a volver con una "
     "nueva habilidad. El mapa se siente como un grafo donde cada zona se conecta con varias más.",
     ["Hallownest es un ejemplo perfecto de diseño de niveles, y la música ayuda muchísimo.",
      "Me perdí durante horas en los Caminos Verdes y aun así quería seguir explorando."]),
    ("Neko", ["terror-cosmico"], ["Lovecraft", "Cthulhu", "Horror cósmico"], "2026-10-05",
     "La llamada de Cthulhu: el miedo a lo desconocido",
     "El relato de Lovecraft no basa su terror en el monstruo, sino en la idea de que la humanidad "
     "es insignificante y el conocimiento puede ser peligroso. Un clásico para entrar al género.",
     ["Leerlo de noche fue mala idea, la parte del marinero Johansen me dejó helado.",
      "Coincido: lo que no se muestra asusta más que cualquier descripción del monstruo."]),

    ("Edgar", ["programacion"], ["Python", "Tipado", "Buenas prácticas"], "2026-09-08",
     "Python tipado: ventajas de los type hints",
     "Los type hints no cambian la ejecución, pero mejoran el autocompletado, la documentación y "
     "permiten detectar errores con mypy antes de llegar a producción.",
     ["Desde que uso mypy en el CI me ahorro muchos errores tontos, buen resumen.",
      "Faltó mencionar `TypedDict` y `Protocol`, pero el artículo es una gran introducción."]),
    ("Edgar", ["videojuegos"], ["RPG", "Soulslike", "Mundo abierto"], "2026-10-12",
     "Elden Ring y la exploración sin guía",
     "El juego te suelta en las Tierras Intermedias sin marcadores ni misiones obvias. La curiosidad "
     "es la brújula: cada ruina y cada cueva esconde algo que merece la pena descubrir.",
     ["Me encantó que no te llevaran de la mano, aunque Margit me costó una semana.",
      "La exploración a caballo con Torrente es de lo mejor que he jugado en mundo abierto."]),

    ("Alan", ["programacion"], ["Rust", "Memoria", "Buenas prácticas"], "2026-09-20",
     "Rust y la seguridad de memoria",
     "El sistema de ownership y el borrow checker garantizan en compilación que no hay accesos "
     "inválidos ni data races. La curva de aprendizaje es real, pero el resultado vale la pena.",
     ["Pelear con el borrow checker es frustrante al principio y adictivo después.",
      "¿Tienes recomendaciones de proyectos pequeños para practicar ownership?"]),
    ("Alan", ["terror-cosmico"], ["Lovecraft", "Antártida", "Horror cósmico"], "2026-10-18",
     "En las montañas de la locura",
     "Una expedición a la Antártida descubre una ciudad milenaria construida por los Antiguos. La "
     "novela mezcla ciencia, exploración y un final que deja una sensación de vacío difícil de olvidar.",
     ["La descripción de los bajorrelieves es mi parte favorita de toda la novela.",
      "Es más lenta que otros textos de Lovecraft, pero el final lo compensa totalmente."]),
    ("Alan", ["videojuegos"], ["RPG", "Narrativa", "Indie"], "2026-11-02",
     "Disco Elysium: el RPG que se juega con el diálogo",
     "Sin combates tradicionales, cada habilidad es una voz en tu cabeza que opina y te contradice. "
     "Es un ejemplo de cómo la escritura puede ser la mecánica principal de un videojuego.",
     ["Nunca había visto un juego donde fallar una tirada fuera tan divertido.",
      "La escritura es increíble; Kim Kitsuragi es de mis personajes favoritos."]),

    ("Jesus", ["programacion"], ["Algoritmos", "Complejidad", "Python"], "2026-09-25",
     "Algoritmos de ordenamiento: cuándo usar cuál",
     "Para pocos elementos la inserción es suficiente; para datos grandes conviene merge sort o "
     "quicksort. En Python, `sorted` usa Timsort, que aprovecha los tramos ya ordenados.",
     ["Muy buena explicación de Timsort, no sabía que aprovechaba los datos casi ordenados.",
      "Me sirvió para repasar complejidad antes del examen de estructuras de datos."]),
    ("Jesus", ["videojuegos", "terror-cosmico"], ["Soulslike", "Lovecraft", "Horror cósmico"], "2026-10-28",
     "Bloodborne: terror cósmico en forma de videojuego",
     "Yharnam combina una ciudad gótica con ideas muy lovecraftianas: la locura como consecuencia de "
     "mirar lo que no se debe y dioses que ni siquiera notan a los humanos.",
     ["La mecánica de Perspicacia es una forma genial de llevar el horror cósmico al juego.",
      "Bloodborne es lo más cercano a Lovecraft que he jugado, y la ambientación es brutal."]),

    ("Amir", ["programacion"], ["Buenas prácticas", "Refactorización"], "2026-09-30",
     "Clean Code en la práctica",
     "Nombres claros, funciones pequeñas y pocas dependencias hacen que el código sea más fácil de "
     "mantener. Refactorizar en pasos pequeños y con pruebas evita romper lo que ya funciona.",
     ["Lo de los nombres claros parece obvio, pero es lo que más cuesta en un equipo.",
      "Añadiría que las pruebas son lo que hace posible refactorizar sin miedo."]),
    ("Amir", ["terror-cosmico"], ["Lovecraft", "Horror cósmico", "Cuento"], "2026-10-22",
     "El color que cayó del cielo",
     "Un meteorito contamina una granja y todo a su alrededor empieza a marchitarse. Es un cuento "
     "donde la amenaza ni siquiera tiene forma, y por eso resulta tan inquietante.",
     ["El horror de algo que no se puede describir está muy bien logrado en este cuento.",
      "Es de mis relatos favoritos de Lovecraft; lo leí en una sola sentada."]),
    ("Amir", ["videojuegos"], ["Roguelike", "Indie", "Narrativa"], "2026-11-10",
     "Hades y el género roguelike",
     "Hades convierte la muerte en parte de la historia: cada intento hace avanzar la trama. Es una "
     "prueba de que un roguelike puede tener narrativa sin perder rejugabilidad.",
     ["Morir y que la historia avance es una idea genial, por eso lo terminé varias veces.",
      "El arte y el doblaje de Hades son de otro nivel dentro del género indie."]),
]


def slug(text: str) -> str:
    table = str.maketrans("áéíóúüñ ", "aeiouun-")
    return text.lower().translate(table)


def build_statements(rng: random.Random) -> list[tuple[str, dict]]:
    stmts: list[tuple[str, dict]] = []

    for name in USERS:
        stmts.append((
            "MERGE (u:User {id: $id}) SET u.name = $name, u.email = $email",
            {"id": f"seed-user-{slug(name)}", "name": name, "email": f"{slug(name)}@uach.mx"},
        ))
    for key, name in CATEGORIES.items():
        stmts.append((
            "MERGE (c:Category {id: $id}) SET c.name = $name, c.url = $url",
            {"id": f"seed-cat-{key}", "name": name, "url": f"{BASE_URL}/categorias/{key}"},
        ))
    for name in TAGS:
        stmts.append((
            "MERGE (t:Tag {id: $id}) SET t.name = $name, t.url = $url",
            {"id": f"seed-tag-{slug(name)}", "name": name, "url": f"{BASE_URL}/tags/{slug(name)}"},
        ))

    for author, cats, tags, date, title, text, comments in ARTICLES:
        article_id = f"seed-art-{slug(title)}"
        article_url = f"{BASE_URL}/articulos/{slug(title)}"
        stmts.append((
            "MATCH (u:User {id: $user_id}) "
            "MERGE (a:Article {id: $id}) "
            "SET a.title = $title, a.date = date($date), a.text = $text "
            "MERGE (u)-[:WROTE]->(a)",
            {"id": article_id, "user_id": f"seed-user-{slug(author)}",
             "title": title, "date": date, "text": text},
        ))
        stmts.append((
            "MATCH (a:Article {id: $id}) MATCH (c:Category) WHERE c.id IN $ids MERGE (a)-[:IN_CATEGORY]->(c)",
            {"id": article_id, "ids": [f"seed-cat-{c}" for c in cats]},
        ))
        stmts.append((
            "MATCH (a:Article {id: $id}) MATCH (t:Tag) WHERE t.id IN $ids MERGE (a)-[:HAS_TAG]->(t)",
            {"id": article_id, "ids": [f"seed-tag-{slug(t)}" for t in tags]},
        ))

        # 2 usuarios al azar (distintos del autor) comentan este artículo.
        commenters = rng.sample([u for u in USERS if u != author], k=2)
        for commenter, comment in zip(commenters, comments):
            stmts.append((
                "MATCH (u:User {id: $user_id}), (a:Article {id: $article_id}) "
                "MERGE (c:Comment {id: $id}) SET c.name = $name, c.url = $url "
                "MERGE (u)-[:POSTED]->(c) "
                "MERGE (a)-[:HAS_COMMENT]->(c)",
                {"id": f"seed-com-{slug(title)}-{slug(commenter)}",
                 "user_id": f"seed-user-{slug(commenter)}", "article_id": article_id,
                 "name": comment, "url": f"{article_url}#comentario-{slug(commenter)}"},
            ))
    return stmts


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga datos de ejemplo en Neo4j.")
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USER", "neo4j"))
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD"))
    parser.add_argument("--database", default=os.getenv("NEO4J_DATABASE") or None)
    parser.add_argument("--seed", type=int, default=42, help="semilla para elegir comentaristas")
    parser.add_argument("--reset", action="store_true", help="borra antes todos los nodos del blog")
    args = parser.parse_args()

    password = args.password or getpass("Contraseña de Neo4j: ")
    service = Neo4jService()
    service.connect(args.uri, args.user, password, args.database)
    try:
        with service._session() as db:
            if args.reset:
                db.write([(
                    "MATCH (n) WHERE n:User OR n:Article OR n:Tag OR n:Category OR n:Comment DETACH DELETE n", {})])
                print("Datos anteriores eliminados.")
            statements = build_statements(random.Random(args.seed))
            db.write(statements)
        print(f"Seed aplicado: {len(USERS)} usuarios, {len(CATEGORIES)} categorías, {len(TAGS)} tags, "
              f"{len(ARTICLES)} artículos y {len(ARTICLES) * 2} comentarios.")
    finally:
        service.close()


if __name__ == "__main__":
    main()
