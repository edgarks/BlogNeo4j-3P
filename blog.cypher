// =====================================================================
// Blog (Neo4j) - restricciones y carga de datos de ejemplo
//
// Modelo:
//   (:User {id, name, email})-[:WROTE]->(:Article {id, title, date, text})
//   (:User)-[:POSTED]->(:Comment {id, name, url})
//   (:Article)-[:HAS_TAG]->(:Tag {id, name, url})
//   (:Article)-[:IN_CATEGORY]->(:Category {id, name, url})
//   (:Article)-[:HAS_COMMENT]->(:Comment)
//
// Es idempotente (IF NOT EXISTS / MERGE): se puede ejecutar varias veces.
// Uso:  cypher-shell -u neo4j -p <password> -f cypher/blog.cypher
// =====================================================================

// ---------------------------------------------------------------------
// Restricciones: `id` único en cada tipo de nodo
// ---------------------------------------------------------------------
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT article_id IF NOT EXISTS FOR (n:Article) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT tag_id IF NOT EXISTS FOR (n:Tag) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT category_id IF NOT EXISTS FOR (n:Category) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT comment_id IF NOT EXISTS FOR (n:Comment) REQUIRE n.id IS UNIQUE;

// ---------------------------------------------------------------------
// (Opcional) Borrar los datos previos del blog
// ---------------------------------------------------------------------
// MATCH (n) WHERE n:User OR n:Article OR n:Tag OR n:Category OR n:Comment DETACH DELETE n;

// ---------------------------------------------------------------------
// Usuarios (5)
// ---------------------------------------------------------------------
MERGE (u:User {id: 'seed-user-neko'}) SET u.name = 'Neko', u.email = 'neko@uach.mx';
MERGE (u:User {id: 'seed-user-edgar'}) SET u.name = 'Edgar', u.email = 'edgar@uach.mx';
MERGE (u:User {id: 'seed-user-alan'}) SET u.name = 'Alan', u.email = 'alan@uach.mx';
MERGE (u:User {id: 'seed-user-jesus'}) SET u.name = 'Jesus', u.email = 'jesus@uach.mx';
MERGE (u:User {id: 'seed-user-amir'}) SET u.name = 'Amir', u.email = 'amir@uach.mx';

// ---------------------------------------------------------------------
// Categorías (3)
// ---------------------------------------------------------------------
MERGE (c:Category {id: 'seed-cat-programacion'}) SET c.name = 'Programación', c.url = 'https://blog.uach.mx/categorias/programacion';
MERGE (c:Category {id: 'seed-cat-videojuegos'}) SET c.name = 'Videojuegos', c.url = 'https://blog.uach.mx/categorias/videojuegos';
MERGE (c:Category {id: 'seed-cat-terror-cosmico'}) SET c.name = 'Libros de terror cósmico', c.url = 'https://blog.uach.mx/categorias/terror-cosmico';

// ---------------------------------------------------------------------
// Tags (24)
// ---------------------------------------------------------------------
MERGE (t:Tag {id: 'seed-tag-neo4j'}) SET t.name = 'Neo4j', t.url = 'https://blog.uach.mx/tags/neo4j';
MERGE (t:Tag {id: 'seed-tag-bases-de-datos'}) SET t.name = 'Bases de datos', t.url = 'https://blog.uach.mx/tags/bases-de-datos';
MERGE (t:Tag {id: 'seed-tag-grafos'}) SET t.name = 'Grafos', t.url = 'https://blog.uach.mx/tags/grafos';
MERGE (t:Tag {id: 'seed-tag-python'}) SET t.name = 'Python', t.url = 'https://blog.uach.mx/tags/python';
MERGE (t:Tag {id: 'seed-tag-tipado'}) SET t.name = 'Tipado', t.url = 'https://blog.uach.mx/tags/tipado';
MERGE (t:Tag {id: 'seed-tag-buenas-practicas'}) SET t.name = 'Buenas prácticas', t.url = 'https://blog.uach.mx/tags/buenas-practicas';
MERGE (t:Tag {id: 'seed-tag-rust'}) SET t.name = 'Rust', t.url = 'https://blog.uach.mx/tags/rust';
MERGE (t:Tag {id: 'seed-tag-memoria'}) SET t.name = 'Memoria', t.url = 'https://blog.uach.mx/tags/memoria';
MERGE (t:Tag {id: 'seed-tag-algoritmos'}) SET t.name = 'Algoritmos', t.url = 'https://blog.uach.mx/tags/algoritmos';
MERGE (t:Tag {id: 'seed-tag-complejidad'}) SET t.name = 'Complejidad', t.url = 'https://blog.uach.mx/tags/complejidad';
MERGE (t:Tag {id: 'seed-tag-refactorizacion'}) SET t.name = 'Refactorización', t.url = 'https://blog.uach.mx/tags/refactorizacion';
MERGE (t:Tag {id: 'seed-tag-metroidvania'}) SET t.name = 'Metroidvania', t.url = 'https://blog.uach.mx/tags/metroidvania';
MERGE (t:Tag {id: 'seed-tag-indie'}) SET t.name = 'Indie', t.url = 'https://blog.uach.mx/tags/indie';
MERGE (t:Tag {id: 'seed-tag-diseno-de-niveles'}) SET t.name = 'Diseño de niveles', t.url = 'https://blog.uach.mx/tags/diseno-de-niveles';
MERGE (t:Tag {id: 'seed-tag-rpg'}) SET t.name = 'RPG', t.url = 'https://blog.uach.mx/tags/rpg';
MERGE (t:Tag {id: 'seed-tag-soulslike'}) SET t.name = 'Soulslike', t.url = 'https://blog.uach.mx/tags/soulslike';
MERGE (t:Tag {id: 'seed-tag-mundo-abierto'}) SET t.name = 'Mundo abierto', t.url = 'https://blog.uach.mx/tags/mundo-abierto';
MERGE (t:Tag {id: 'seed-tag-narrativa'}) SET t.name = 'Narrativa', t.url = 'https://blog.uach.mx/tags/narrativa';
MERGE (t:Tag {id: 'seed-tag-roguelike'}) SET t.name = 'Roguelike', t.url = 'https://blog.uach.mx/tags/roguelike';
MERGE (t:Tag {id: 'seed-tag-lovecraft'}) SET t.name = 'Lovecraft', t.url = 'https://blog.uach.mx/tags/lovecraft';
MERGE (t:Tag {id: 'seed-tag-cthulhu'}) SET t.name = 'Cthulhu', t.url = 'https://blog.uach.mx/tags/cthulhu';
MERGE (t:Tag {id: 'seed-tag-horror-cosmico'}) SET t.name = 'Horror cósmico', t.url = 'https://blog.uach.mx/tags/horror-cosmico';
MERGE (t:Tag {id: 'seed-tag-antartida'}) SET t.name = 'Antártida', t.url = 'https://blog.uach.mx/tags/antartida';
MERGE (t:Tag {id: 'seed-tag-cuento'}) SET t.name = 'Cuento', t.url = 'https://blog.uach.mx/tags/cuento';

// ---------------------------------------------------------------------
// Artículos (13), con sus relaciones y comentarios
// ---------------------------------------------------------------------

// Por qué los grafos modelan mejor las relaciones
MATCH (u:User {id: 'seed-user-neko'})
MERGE (a:Article {id: 'seed-art-por-que-los-grafos-modelan-mejor-las-relaciones'})
SET a.title = 'Por qué los grafos modelan mejor las relaciones', a.date = date('2026-09-02'), a.text = 'Cuando los datos están muy conectados, como usuarios, artículos y comentarios, una base de grafos evita los JOIN encadenados. En Neo4j las relaciones son ciudadanos de primera clase y se recorren con Cypher de forma natural.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-por-que-los-grafos-modelan-mejor-las-relaciones'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-programacion'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-por-que-los-grafos-modelan-mejor-las-relaciones'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-neo4j', 'seed-tag-bases-de-datos', 'seed-tag-grafos'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-edgar'}), (a:Article {id: 'seed-art-por-que-los-grafos-modelan-mejor-las-relaciones'})
MERGE (c:Comment {id: 'seed-com-por-que-los-grafos-modelan-mejor-las-relaciones-edgar'})
SET c.name = 'Justo lo que necesitaba para el proyecto de la clase, gracias por la comparación.', c.url = 'https://blog.uach.mx/articulos/por-que-los-grafos-modelan-mejor-las-relaciones#comentario-edgar'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-amir'}), (a:Article {id: 'seed-art-por-que-los-grafos-modelan-mejor-las-relaciones'})
MERGE (c:Comment {id: 'seed-com-por-que-los-grafos-modelan-mejor-las-relaciones-amir'})
SET c.name = 'Los JOIN de cinco tablas me dieron pesadillas; Cypher se lee mucho mejor.', c.url = 'https://blog.uach.mx/articulos/por-que-los-grafos-modelan-mejor-las-relaciones#comentario-amir'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Hollow Knight: diseño de un mundo interconectado
MATCH (u:User {id: 'seed-user-neko'})
MERGE (a:Article {id: 'seed-art-hollow-knight:-diseno-de-un-mundo-interconectado'})
SET a.title = 'Hollow Knight: diseño de un mundo interconectado', a.date = date('2026-09-15'), a.text = 'Hallownest funciona porque cada atajo y cada puerta bloqueada te invita a volver con una nueva habilidad. El mapa se siente como un grafo donde cada zona se conecta con varias más.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-hollow-knight:-diseno-de-un-mundo-interconectado'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-videojuegos'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-hollow-knight:-diseno-de-un-mundo-interconectado'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-metroidvania', 'seed-tag-indie', 'seed-tag-diseno-de-niveles'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-jesus'}), (a:Article {id: 'seed-art-hollow-knight:-diseno-de-un-mundo-interconectado'})
MERGE (c:Comment {id: 'seed-com-hollow-knight:-diseno-de-un-mundo-interconectado-jesus'})
SET c.name = 'Hallownest es un ejemplo perfecto de diseño de niveles, y la música ayuda muchísimo.', c.url = 'https://blog.uach.mx/articulos/hollow-knight:-diseno-de-un-mundo-interconectado#comentario-jesus'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-edgar'}), (a:Article {id: 'seed-art-hollow-knight:-diseno-de-un-mundo-interconectado'})
MERGE (c:Comment {id: 'seed-com-hollow-knight:-diseno-de-un-mundo-interconectado-edgar'})
SET c.name = 'Me perdí durante horas en los Caminos Verdes y aun así quería seguir explorando.', c.url = 'https://blog.uach.mx/articulos/hollow-knight:-diseno-de-un-mundo-interconectado#comentario-edgar'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// La llamada de Cthulhu: el miedo a lo desconocido
MATCH (u:User {id: 'seed-user-neko'})
MERGE (a:Article {id: 'seed-art-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido'})
SET a.title = 'La llamada de Cthulhu: el miedo a lo desconocido', a.date = date('2026-10-05'), a.text = 'El relato de Lovecraft no basa su terror en el monstruo, sino en la idea de que la humanidad es insignificante y el conocimiento puede ser peligroso. Un clásico para entrar al género.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-terror-cosmico'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-lovecraft', 'seed-tag-cthulhu', 'seed-tag-horror-cosmico'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-alan'}), (a:Article {id: 'seed-art-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido'})
MERGE (c:Comment {id: 'seed-com-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido-alan'})
SET c.name = 'Leerlo de noche fue mala idea, la parte del marinero Johansen me dejó helado.', c.url = 'https://blog.uach.mx/articulos/la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido#comentario-alan'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-edgar'}), (a:Article {id: 'seed-art-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido'})
MERGE (c:Comment {id: 'seed-com-la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido-edgar'})
SET c.name = 'Coincido: lo que no se muestra asusta más que cualquier descripción del monstruo.', c.url = 'https://blog.uach.mx/articulos/la-llamada-de-cthulhu:-el-miedo-a-lo-desconocido#comentario-edgar'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Python tipado: ventajas de los type hints
MATCH (u:User {id: 'seed-user-edgar'})
MERGE (a:Article {id: 'seed-art-python-tipado:-ventajas-de-los-type-hints'})
SET a.title = 'Python tipado: ventajas de los type hints', a.date = date('2026-09-08'), a.text = 'Los type hints no cambian la ejecución, pero mejoran el autocompletado, la documentación y permiten detectar errores con mypy antes de llegar a producción.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-python-tipado:-ventajas-de-los-type-hints'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-programacion'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-python-tipado:-ventajas-de-los-type-hints'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-python', 'seed-tag-tipado', 'seed-tag-buenas-practicas'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-python-tipado:-ventajas-de-los-type-hints'})
MERGE (c:Comment {id: 'seed-com-python-tipado:-ventajas-de-los-type-hints-neko'})
SET c.name = 'Desde que uso mypy en el CI me ahorro muchos errores tontos, buen resumen.', c.url = 'https://blog.uach.mx/articulos/python-tipado:-ventajas-de-los-type-hints#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-jesus'}), (a:Article {id: 'seed-art-python-tipado:-ventajas-de-los-type-hints'})
MERGE (c:Comment {id: 'seed-com-python-tipado:-ventajas-de-los-type-hints-jesus'})
SET c.name = 'Faltó mencionar `TypedDict` y `Protocol`, pero el artículo es una gran introducción.', c.url = 'https://blog.uach.mx/articulos/python-tipado:-ventajas-de-los-type-hints#comentario-jesus'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Elden Ring y la exploración sin guía
MATCH (u:User {id: 'seed-user-edgar'})
MERGE (a:Article {id: 'seed-art-elden-ring-y-la-exploracion-sin-guia'})
SET a.title = 'Elden Ring y la exploración sin guía', a.date = date('2026-10-12'), a.text = 'El juego te suelta en las Tierras Intermedias sin marcadores ni misiones obvias. La curiosidad es la brújula: cada ruina y cada cueva esconde algo que merece la pena descubrir.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-elden-ring-y-la-exploracion-sin-guia'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-videojuegos'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-elden-ring-y-la-exploracion-sin-guia'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-rpg', 'seed-tag-soulslike', 'seed-tag-mundo-abierto'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-elden-ring-y-la-exploracion-sin-guia'})
MERGE (c:Comment {id: 'seed-com-elden-ring-y-la-exploracion-sin-guia-neko'})
SET c.name = 'Me encantó que no te llevaran de la mano, aunque Margit me costó una semana.', c.url = 'https://blog.uach.mx/articulos/elden-ring-y-la-exploracion-sin-guia#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-jesus'}), (a:Article {id: 'seed-art-elden-ring-y-la-exploracion-sin-guia'})
MERGE (c:Comment {id: 'seed-com-elden-ring-y-la-exploracion-sin-guia-jesus'})
SET c.name = 'La exploración a caballo con Torrente es de lo mejor que he jugado en mundo abierto.', c.url = 'https://blog.uach.mx/articulos/elden-ring-y-la-exploracion-sin-guia#comentario-jesus'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Rust y la seguridad de memoria
MATCH (u:User {id: 'seed-user-alan'})
MERGE (a:Article {id: 'seed-art-rust-y-la-seguridad-de-memoria'})
SET a.title = 'Rust y la seguridad de memoria', a.date = date('2026-09-20'), a.text = 'El sistema de ownership y el borrow checker garantizan en compilación que no hay accesos inválidos ni data races. La curva de aprendizaje es real, pero el resultado vale la pena.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-rust-y-la-seguridad-de-memoria'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-programacion'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-rust-y-la-seguridad-de-memoria'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-rust', 'seed-tag-memoria', 'seed-tag-buenas-practicas'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-amir'}), (a:Article {id: 'seed-art-rust-y-la-seguridad-de-memoria'})
MERGE (c:Comment {id: 'seed-com-rust-y-la-seguridad-de-memoria-amir'})
SET c.name = 'Pelear con el borrow checker es frustrante al principio y adictivo después.', c.url = 'https://blog.uach.mx/articulos/rust-y-la-seguridad-de-memoria#comentario-amir'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-rust-y-la-seguridad-de-memoria'})
MERGE (c:Comment {id: 'seed-com-rust-y-la-seguridad-de-memoria-neko'})
SET c.name = '¿Tienes recomendaciones de proyectos pequeños para practicar ownership?', c.url = 'https://blog.uach.mx/articulos/rust-y-la-seguridad-de-memoria#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// En las montañas de la locura
MATCH (u:User {id: 'seed-user-alan'})
MERGE (a:Article {id: 'seed-art-en-las-montanas-de-la-locura'})
SET a.title = 'En las montañas de la locura', a.date = date('2026-10-18'), a.text = 'Una expedición a la Antártida descubre una ciudad milenaria construida por los Antiguos. La novela mezcla ciencia, exploración y un final que deja una sensación de vacío difícil de olvidar.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-en-las-montanas-de-la-locura'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-terror-cosmico'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-en-las-montanas-de-la-locura'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-lovecraft', 'seed-tag-antartida', 'seed-tag-horror-cosmico'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-en-las-montanas-de-la-locura'})
MERGE (c:Comment {id: 'seed-com-en-las-montanas-de-la-locura-neko'})
SET c.name = 'La descripción de los bajorrelieves es mi parte favorita de toda la novela.', c.url = 'https://blog.uach.mx/articulos/en-las-montanas-de-la-locura#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-amir'}), (a:Article {id: 'seed-art-en-las-montanas-de-la-locura'})
MERGE (c:Comment {id: 'seed-com-en-las-montanas-de-la-locura-amir'})
SET c.name = 'Es más lenta que otros textos de Lovecraft, pero el final lo compensa totalmente.', c.url = 'https://blog.uach.mx/articulos/en-las-montanas-de-la-locura#comentario-amir'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Disco Elysium: el RPG que se juega con el diálogo
MATCH (u:User {id: 'seed-user-alan'})
MERGE (a:Article {id: 'seed-art-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo'})
SET a.title = 'Disco Elysium: el RPG que se juega con el diálogo', a.date = date('2026-11-02'), a.text = 'Sin combates tradicionales, cada habilidad es una voz en tu cabeza que opina y te contradice. Es un ejemplo de cómo la escritura puede ser la mecánica principal de un videojuego.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-videojuegos'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-rpg', 'seed-tag-narrativa', 'seed-tag-indie'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-edgar'}), (a:Article {id: 'seed-art-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo'})
MERGE (c:Comment {id: 'seed-com-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo-edgar'})
SET c.name = 'Nunca había visto un juego donde fallar una tirada fuera tan divertido.', c.url = 'https://blog.uach.mx/articulos/disco-elysium:-el-rpg-que-se-juega-con-el-dialogo#comentario-edgar'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo'})
MERGE (c:Comment {id: 'seed-com-disco-elysium:-el-rpg-que-se-juega-con-el-dialogo-neko'})
SET c.name = 'La escritura es increíble; Kim Kitsuragi es de mis personajes favoritos.', c.url = 'https://blog.uach.mx/articulos/disco-elysium:-el-rpg-que-se-juega-con-el-dialogo#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Algoritmos de ordenamiento: cuándo usar cuál
MATCH (u:User {id: 'seed-user-jesus'})
MERGE (a:Article {id: 'seed-art-algoritmos-de-ordenamiento:-cuando-usar-cual'})
SET a.title = 'Algoritmos de ordenamiento: cuándo usar cuál', a.date = date('2026-09-25'), a.text = 'Para pocos elementos la inserción es suficiente; para datos grandes conviene merge sort o quicksort. En Python, `sorted` usa Timsort, que aprovecha los tramos ya ordenados.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-algoritmos-de-ordenamiento:-cuando-usar-cual'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-programacion'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-algoritmos-de-ordenamiento:-cuando-usar-cual'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-algoritmos', 'seed-tag-complejidad', 'seed-tag-python'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-algoritmos-de-ordenamiento:-cuando-usar-cual'})
MERGE (c:Comment {id: 'seed-com-algoritmos-de-ordenamiento:-cuando-usar-cual-neko'})
SET c.name = 'Muy buena explicación de Timsort, no sabía que aprovechaba los datos casi ordenados.', c.url = 'https://blog.uach.mx/articulos/algoritmos-de-ordenamiento:-cuando-usar-cual#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-alan'}), (a:Article {id: 'seed-art-algoritmos-de-ordenamiento:-cuando-usar-cual'})
MERGE (c:Comment {id: 'seed-com-algoritmos-de-ordenamiento:-cuando-usar-cual-alan'})
SET c.name = 'Me sirvió para repasar complejidad antes del examen de estructuras de datos.', c.url = 'https://blog.uach.mx/articulos/algoritmos-de-ordenamiento:-cuando-usar-cual#comentario-alan'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Bloodborne: terror cósmico en forma de videojuego
MATCH (u:User {id: 'seed-user-jesus'})
MERGE (a:Article {id: 'seed-art-bloodborne:-terror-cosmico-en-forma-de-videojuego'})
SET a.title = 'Bloodborne: terror cósmico en forma de videojuego', a.date = date('2026-10-28'), a.text = 'Yharnam combina una ciudad gótica con ideas muy lovecraftianas: la locura como consecuencia de mirar lo que no se debe y dioses que ni siquiera notan a los humanos.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-bloodborne:-terror-cosmico-en-forma-de-videojuego'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-videojuegos', 'seed-cat-terror-cosmico'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-bloodborne:-terror-cosmico-en-forma-de-videojuego'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-soulslike', 'seed-tag-lovecraft', 'seed-tag-horror-cosmico'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-edgar'}), (a:Article {id: 'seed-art-bloodborne:-terror-cosmico-en-forma-de-videojuego'})
MERGE (c:Comment {id: 'seed-com-bloodborne:-terror-cosmico-en-forma-de-videojuego-edgar'})
SET c.name = 'La mecánica de Perspicacia es una forma genial de llevar el horror cósmico al juego.', c.url = 'https://blog.uach.mx/articulos/bloodborne:-terror-cosmico-en-forma-de-videojuego#comentario-edgar'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-alan'}), (a:Article {id: 'seed-art-bloodborne:-terror-cosmico-en-forma-de-videojuego'})
MERGE (c:Comment {id: 'seed-com-bloodborne:-terror-cosmico-en-forma-de-videojuego-alan'})
SET c.name = 'Bloodborne es lo más cercano a Lovecraft que he jugado, y la ambientación es brutal.', c.url = 'https://blog.uach.mx/articulos/bloodborne:-terror-cosmico-en-forma-de-videojuego#comentario-alan'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Clean Code en la práctica
MATCH (u:User {id: 'seed-user-amir'})
MERGE (a:Article {id: 'seed-art-clean-code-en-la-practica'})
SET a.title = 'Clean Code en la práctica', a.date = date('2026-09-30'), a.text = 'Nombres claros, funciones pequeñas y pocas dependencias hacen que el código sea más fácil de mantener. Refactorizar en pasos pequeños y con pruebas evita romper lo que ya funciona.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-clean-code-en-la-practica'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-programacion'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-clean-code-en-la-practica'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-buenas-practicas', 'seed-tag-refactorizacion'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-jesus'}), (a:Article {id: 'seed-art-clean-code-en-la-practica'})
MERGE (c:Comment {id: 'seed-com-clean-code-en-la-practica-jesus'})
SET c.name = 'Lo de los nombres claros parece obvio, pero es lo que más cuesta en un equipo.', c.url = 'https://blog.uach.mx/articulos/clean-code-en-la-practica#comentario-jesus'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-clean-code-en-la-practica'})
MERGE (c:Comment {id: 'seed-com-clean-code-en-la-practica-neko'})
SET c.name = 'Añadiría que las pruebas son lo que hace posible refactorizar sin miedo.', c.url = 'https://blog.uach.mx/articulos/clean-code-en-la-practica#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// El color que cayó del cielo
MATCH (u:User {id: 'seed-user-amir'})
MERGE (a:Article {id: 'seed-art-el-color-que-cayo-del-cielo'})
SET a.title = 'El color que cayó del cielo', a.date = date('2026-10-22'), a.text = 'Un meteorito contamina una granja y todo a su alrededor empieza a marchitarse. Es un cuento donde la amenaza ni siquiera tiene forma, y por eso resulta tan inquietante.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-el-color-que-cayo-del-cielo'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-terror-cosmico'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-el-color-que-cayo-del-cielo'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-lovecraft', 'seed-tag-horror-cosmico', 'seed-tag-cuento'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-jesus'}), (a:Article {id: 'seed-art-el-color-que-cayo-del-cielo'})
MERGE (c:Comment {id: 'seed-com-el-color-que-cayo-del-cielo-jesus'})
SET c.name = 'El horror de algo que no se puede describir está muy bien logrado en este cuento.', c.url = 'https://blog.uach.mx/articulos/el-color-que-cayo-del-cielo#comentario-jesus'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-alan'}), (a:Article {id: 'seed-art-el-color-que-cayo-del-cielo'})
MERGE (c:Comment {id: 'seed-com-el-color-que-cayo-del-cielo-alan'})
SET c.name = 'Es de mis relatos favoritos de Lovecraft; lo leí en una sola sentada.', c.url = 'https://blog.uach.mx/articulos/el-color-que-cayo-del-cielo#comentario-alan'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);

// Hades y el género roguelike
MATCH (u:User {id: 'seed-user-amir'})
MERGE (a:Article {id: 'seed-art-hades-y-el-genero-roguelike'})
SET a.title = 'Hades y el género roguelike', a.date = date('2026-11-10'), a.text = 'Hades convierte la muerte en parte de la historia: cada intento hace avanzar la trama. Es una prueba de que un roguelike puede tener narrativa sin perder rejugabilidad.'
MERGE (u)-[:WROTE]->(a);
MATCH (a:Article {id: 'seed-art-hades-y-el-genero-roguelike'}) MATCH (c:Category) WHERE c.id IN ['seed-cat-videojuegos'] MERGE (a)-[:IN_CATEGORY]->(c);
MATCH (a:Article {id: 'seed-art-hades-y-el-genero-roguelike'}) MATCH (t:Tag) WHERE t.id IN ['seed-tag-roguelike', 'seed-tag-indie', 'seed-tag-narrativa'] MERGE (a)-[:HAS_TAG]->(t);
MATCH (u:User {id: 'seed-user-alan'}), (a:Article {id: 'seed-art-hades-y-el-genero-roguelike'})
MERGE (c:Comment {id: 'seed-com-hades-y-el-genero-roguelike-alan'})
SET c.name = 'Morir y que la historia avance es una idea genial, por eso lo terminé varias veces.', c.url = 'https://blog.uach.mx/articulos/hades-y-el-genero-roguelike#comentario-alan'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
MATCH (u:User {id: 'seed-user-neko'}), (a:Article {id: 'seed-art-hades-y-el-genero-roguelike'})
MERGE (c:Comment {id: 'seed-com-hades-y-el-genero-roguelike-neko'})
SET c.name = 'El arte y el doblaje de Hades son de otro nivel dentro del género indie.', c.url = 'https://blog.uach.mx/articulos/hades-y-el-genero-roguelike#comentario-neko'
MERGE (u)-[:POSTED]->(c)
MERGE (a)-[:HAS_COMMENT]->(c);
