-- 1. LIMPIEZA (Orden inverso para evitar errores de FK) -----------------------------------------------
DROP VIEW IF EXISTS V_USUARIOS_PROMEDIO_DESTACADO;
DROP VIEW IF EXISTS V_RANKING_TOKENS_TRIMESTRAL;
DROP VIEW IF EXISTS V_ESTADISTICAS_MODULOS;
DROP VIEW IF EXISTS V_ACTIVIDAD_USUARIOS_TOTAL;

DROP TABLE IF EXISTS HISTORICO_TOKENS;
DROP TABLE IF EXISTS RESPUESTAS;
DROP TABLE IF EXISTS POSTS;
DROP TABLE IF EXISTS MATRICULAS;
DROP TABLE IF EXISTS MODULOS;
DROP TABLE IF EXISTS USUARIOS;

-- 2. CREACIÓN DE TABLAS ----------------------------------------------------------------------------

CREATE TABLE USUARIOS (
    id_usuario        INT NOT NULL AUTO_INCREMENT,
    username          VARCHAR(50) NOT NULL,
    email_usuario     VARCHAR(100) NOT NULL,
    password_usuario  VARCHAR(255) NOT NULL,
    fecha_alta        DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tokens            INT DEFAULT 0,
    rol               VARCHAR(50) NOT NULL,
    imagen_usuario    VARCHAR(150),
    is_active         BOOLEAN DEFAULT FALSE NOT NULL,

    CONSTRAINT pk_USUARIOS PRIMARY KEY (id_usuario),
    CONSTRAINT uq_email UNIQUE (email_usuario),    
    CONSTRAINT cb_rol CHECK (rol IN ('ALUMNO', 'PROFESOR', 'ADMINISTRADOR'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE MODULOS (
    codigo_modulo      VARCHAR(50) NOT NULL,
    nombre_asignatura  VARCHAR(100) NOT NULL,
    curso_modulo       VARCHAR(50) NOT NULL,
    is_deleted         BOOLEAN DEFAULT FALSE NOT NULL,
    
    CONSTRAINT pk_MODULOS PRIMARY KEY (codigo_modulo),
    CONSTRAINT uq_asignatura UNIQUE (nombre_asignatura)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE MATRICULAS (
    id_usuario     INT NOT NULL,
    codigo_modulo  VARCHAR(50) NOT NULL,
    fecha_inicio   DATETIME NOT NULL,
    fecha_final    DATETIME NOT NULL,
    
    CONSTRAINT pk_MATRICULAS PRIMARY KEY (id_usuario, codigo_modulo),
    CONSTRAINT fk_MATRICULAS_USUARIOS FOREIGN KEY (id_usuario) 
        REFERENCES USUARIOS (id_usuario) ON DELETE CASCADE,
    CONSTRAINT fk_MATRICULAS_MODULOS FOREIGN KEY (codigo_modulo) 
        REFERENCES MODULOS (codigo_modulo) ON DELETE CASCADE,
    CONSTRAINT ck_VIGENCIA CHECK (fecha_final > fecha_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE POSTS (
    id_post              INT NOT NULL AUTO_INCREMENT,
    titulo_post          VARCHAR(150) NOT NULL,
    contenido_post       TEXT NOT NULL,
    fecha_creacion_post  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id_usuario           INT NULL,
    codigo_modulo        VARCHAR(50) NOT NULL,
    imagen_post          VARCHAR(150),
    is_deleted           BOOLEAN DEFAULT FALSE NOT NULL,
    
    CONSTRAINT pk_POSTS PRIMARY KEY (id_post),
    CONSTRAINT fk_POSTS_USUARIOS FOREIGN KEY (id_usuario) 
        REFERENCES USUARIOS (id_usuario) ON DELETE SET NULL,
    CONSTRAINT fk_POSTS_MODULOS FOREIGN KEY (codigo_modulo) 
        REFERENCES MODULOS (codigo_modulo) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE RESPUESTAS (
    id_respuesta         INT NOT NULL AUTO_INCREMENT,
    contenido_respuesta  TEXT NOT NULL,
    fecha_respuesta      DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id_post              INT NOT NULL,
    id_usuario           INT NULL,
    es_mejor_respuesta   BOOLEAN DEFAULT FALSE NOT NULL,
    imagen_respuesta     VARCHAR(150),
    is_deleted           BOOLEAN DEFAULT FALSE NOT NULL,
    
    CONSTRAINT pk_RESPUESTAS PRIMARY KEY (id_respuesta),
    CONSTRAINT fk_RESPUESTAS_POSTS FOREIGN KEY (id_post) 
        REFERENCES POSTS (id_post) ON DELETE RESTRICT,
    CONSTRAINT fk_RESPUESTAS_USUARIOS FOREIGN KEY (id_usuario) 
        REFERENCES USUARIOS (id_usuario) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE HISTORICO_TOKENS (
    id_tokens     INT NOT NULL AUTO_INCREMENT,
    tokens        INT NOT NULL,
    fecha_tokens  DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    motivo        VARCHAR(100) NOT NULL,
    trimestre     VARCHAR(50) NOT NULL,
    id_usuario    INT NOT NULL,
    
    CONSTRAINT pk_HISTORICO_TOKENS PRIMARY KEY (id_tokens),
    CONSTRAINT fk_TOKENS_USUARIOS FOREIGN KEY (id_usuario) 
        REFERENCES USUARIOS (id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 3. INSERCIÓN DE USUARIOS ------------------------------------------------------------------

-- Nota: is_active = 1 (TRUE), is_active = 0 (FALSE)
INSERT INTO USUARIOS (username, email_usuario, password_usuario, rol, is_active) VALUES
('hpotter', 'potter@pixys.com', 'hash_hp123', 'ALUMNO', 1),
('hgranger', 'granger@pixys.com', 'hash_hg777', 'ALUMNO', 1),
('ssnape', 'snape@pixys.com', 'hash_profe456', 'PROFESOR', 1),
('rweasley', 'ron@pixys.com', 'hash_rw999', 'ALUMNO', 1),
('llovegood', 'luna@pixys.com', 'hash_ll888', 'ALUMNO', 0), -- Inactivo para probar
('nlupin', 'lupin@pixys.com', 'hash_remus890', 'PROFESOR', 1),
('cdiggory', 'cedric@pixys.com', 'hash_ced321', 'ALUMNO', 1),
('nevilleb', 'longbottom@pixys.com', 'hash_nev444', 'ALUMNO', 1),
('gweasley', 'ginny@pixys.com', 'hash_gw555', 'ALUMNO', 1),
('dmalfoy', 'draco@pixys.com', 'hash_dm666', 'ALUMNO', 1);

--  INSERCIÓN DE MÓDULOS ---------------------------------------------------------------------
INSERT INTO MODULOS (codigo_modulo, nombre_asignatura, curso_modulo) VALUES
('MOD-BBDD', 'Bases de Datos Avanzadas', '1º DAW'),
('MOD-PROG', 'Programación', '1º DAW'),
('MOD-ENT', 'Entornos de Desarrollo', '1º DAW');


--  INSERCIÓN DE MATRICULAS ------------------------------------------------------------------
INSERT INTO MATRICULAS (id_usuario, codigo_modulo, fecha_inicio, fecha_final) VALUES
(1, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(2, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(4, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(1, 'MOD-PROG', '2026-09-01', '2027-06-30'),
(6, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(7, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(8, 'MOD-PROG', '2026-09-01', '2027-06-30'),
(9, 'MOD-PROG', '2026-09-01', '2027-06-30'),
(6, 'MOD-ENT', '2026-09-01', '2027-06-30');

--  INSERCIÓN DE POSTS ------------------------------------------------------------------------
-- Generamos actividad para que la consulta de "promedio" y "módulo popular" tengan datos
INSERT INTO POSTS (titulo_post, contenido_post, id_usuario, codigo_modulo) VALUES
('Duda Joins', '¿Diferencia entre Inner y Left?', 1, 'MOD-BBDD'),
('Duda SQL', '¿Como se hace un grupo by?', 1, 'MOD-BBDD'),
('Examen', '¿Qué entra en el examen?', 2, 'MOD-BBDD'),
('Funciones', '¿Cómo funcionan los métodos?', 4, 'MOD-PROG'),
('Error con Foreign Keys', 'No me deja borrar un registro de la tabla padre...', 2, 'MOD-BBDD'),
('Optimización de índices', '¿Cuándo conviene crear un índice compuesto?', 2, 'MOD-BBDD'),
('Problema con bucle For', 'Se me queda un bucle infinito al recorrer un array', 6, 'MOD-PROG'),
('Duda con Git Merge', '¿Qué diferencia hay entre merge y rebase?', 7, 'MOD-ENT'),
('Configuración de Entorno', 'Instalación de extensiones recomendadas en VSCode', 1, 'MOD-ENT'),
('Sintaxis de subconsultas', 'Ejemplos de subconsultas correlacionadas en WHERE', 2, 'MOD-BBDD');

-- INSERCIÓN DE RESPUESTAS -------------------------------------------------------------------
INSERT INTO RESPUESTAS (contenido_respuesta, id_post, id_usuario, es_mejor_respuesta) VALUES
('El Inner solo trae coincidencias...', 1, 2, TRUE),
('Usa GROUP BY para agrupar...', 2, 3, FALSE),
('Entra todo el temario de SQL', 3, 3, TRUE),
('Eso es por la restricción ON DELETE RESTRICT que le pusiste.', 5, 3, TRUE),
('Depende de los campos que uses habitualmente en el WHERE.', 6, 5, FALSE),
('Revisa la condición de parada del bucle, el contador no se está incrementando.', 7, 3, TRUE),
('Merge une las ramas en un commit nuevo; rebase desplaza la base de tu rama.', 8, 5, FALSE),
('El rebase reescribe el histórico, ten cuidado si trabajas en equipo.', 8, 3, TRUE),
('Instala Prettier y GitLens, te facilitarán mucho la vida.', 9, 7, FALSE);

--  INSERCIÓN DE HISTORICO_TOKENS ------------------------------------------------------------
INSERT INTO HISTORICO_TOKENS (tokens, motivo, trimestre, id_usuario) VALUES
(20, 'MEJOR_RESPUESTA', '2026_T1', 1),
(10, 'PARTICIPACION', '2026_T1', 2),
(50, 'PROFESOR_EXCELENCIA', '2026_T1', 4),
(35, 'APORTACION_EXCEPCIONAL_COMUNIDAD', '2026_T1', 2),
(5, 'CORRECCION_MENOR_SINTAXIS', '2026_T1', 6),
(40, 'RESOLUCION_BUG_COMPLEJO', '2026_T1', 7),
(15, 'COLABORACION_COMPAÑERO', '2026_T1', 1),
(60, 'PREMIO_PROYECTO_DESTACADO', '2026_T1', 2);

-- 4. CONSULTAS COMPLEJAS --------------------------------------------------------------------

SELECT u.username, COUNT(p.id_post) AS posts_realizados
FROM USUARIOS u
JOIN POSTS p ON u.id_usuario = p.id_usuario
GROUP BY u.id_usuario
HAVING posts_realizados > (
    SELECT AVG(total_usuario)
    FROM (
        SELECT COUNT(id_post) AS total_usuario 
        FROM POSTS 
        GROUP BY id_usuario
    ) AS subconsulta_promedio
);

SELECT u.username, m.nombre_asignatura, COUNT(p.id_post) AS posts_este_mes
FROM POSTS p
JOIN USUARIOS u ON p.id_usuario = u.id_usuario
JOIN MODULOS m ON p.codigo_modulo = m.codigo_modulo
WHERE MONTH(p.fecha_creacion_post) = MONTH(NOW())
AND YEAR(p.fecha_creacion_post) = YEAR(NOW())
AND p.codigo_modulo = (
      SELECT codigo_modulo 
      FROM POSTS 
      GROUP BY codigo_modulo 
      ORDER BY COUNT(id_post) DESC 
      LIMIT 1
  )
GROUP BY u.id_usuario, m.nombre_asignatura;

SELECT u.id_usuario, ht.tokens AS tokens_transaccion,  ht.motivo,  ht.fecha_tokens
FROM usuarios u
JOIN historico_tokens ht ON (u.id_usuario = ht.id_usuario)
WHERE ht.tokens > (
    SELECT AVG(ABS(ht2.tokens))
    FROM historico_tokens ht2
    WHERE MONTH(ht2.fecha_tokens) = MONTH(NOW())
    AND YEAR(ht2.fecha_tokens) = YEAR(NOW())
)
AND MONTH(ht.fecha_tokens) = MONTH(NOW())
AND YEAR(ht.fecha_tokens) = YEAR(NOW())
ORDER BY ht.tokens DESC;

SELECT m.nombre_asignatura, 
       COUNT(DISTINCT p.id_post) AS total_posts, 
       COUNT(r.id_respuesta) AS total_respuestas,
       IFNULL(COUNT(r.id_respuesta) / NULLIF(COUNT(DISTINCT p.id_post), 0), 0) AS promedio_respuestas_por_post
FROM MODULOS m 
LEFT JOIN POSTS p ON m.codigo_modulo = p.codigo_modulo
LEFT JOIN RESPUESTAS r ON p.id_post = r.id_post
GROUP BY m.codigo_modulo
ORDER BY promedio_respuestas_por_post DESC;


-- 5. CREACION DE VISTAS -------------------------------------------------------------------------------------------

CREATE VIEW V_ACTIVIDAD_USUARIOS_TOTAL AS
SELECT
u.id_usuario,
u.username,
COUNT(DISTINCT p.id_post) AS posts_totales,
COUNT(DISTINCT r.id_respuesta) AS respuestas_totales,
IFNULL(SUM(DISTINCT ht.tokens), 0) AS balance_tokens_actual
FROM USUARIOS u
LEFT JOIN POSTS p ON u.id_usuario = p.id_usuario
LEFT JOIN RESPUESTAS r ON u.id_usuario = r.id_usuario
LEFT JOIN HISTORICO_TOKENS ht ON u.id_usuario = ht.id_usuario
GROUP BY u.id_usuario, u.username;

CREATE VIEW V_ESTADISTICAS_MODULOS AS
SELECT 
    m.nombre_asignatura,
    COUNT(DISTINCT p.id_post) AS posts_totales,
    COUNT(r.id_respuesta) AS respuestas_totales,
    IFNULL(COUNT(r.id_respuesta) / NULLIF(COUNT(DISTINCT p.id_post), 0), 0) AS promedio_respuestas_por_post
FROM MODULOS m
LEFT JOIN POSTS p ON m.codigo_modulo = p.codigo_modulo
LEFT JOIN RESPUESTAS r ON p.id_post = r.id_post
GROUP BY m.codigo_modulo, m.nombre_asignatura;

CREATE VIEW V_RANKING_TOKENS_TRIMESTRAL AS
SELECT 
    u.id_usuario,
    u.username,
    ht.trimestre,
    SUM(ht.tokens) AS tokens_totales_trimestre
FROM USUARIOS u
JOIN HISTORICO_TOKENS ht ON u.id_usuario = ht.id_usuario
GROUP BY u.id_usuario, u.username, ht.trimestre;

CREATE VIEW V_USUARIOS_PROMEDIO_DESTACADO AS
SELECT 
    u.id_usuario,
    u.username,
    COUNT(p.id_post) AS posts_realizados
FROM USUARIOS u
JOIN POSTS p ON u.id_usuario = p.id_usuario
GROUP BY u.id_usuario, u.username
HAVING posts_realizados > (
    SELECT AVG(total_usuario)
    FROM (
        SELECT COUNT(id_post) AS total_usuario
        FROM POSTS
        GROUP BY id_usuario
    ) AS subconsulta_promedio
);