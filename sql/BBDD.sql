-- 1. LIMPIEZA (Orden inverso para evitar errores de FK)
DROP TABLE IF EXISTS HISTORICO_TOKENS;
DROP TABLE IF EXISTS RESPUESTAS;
DROP TABLE IF EXISTS POSTS;
DROP TABLE IF EXISTS MATRICULAS;
DROP TABLE IF EXISTS MODULOS;
DROP TABLE IF EXISTS USUARIOS;

-- 2. CREACIÓN DE TABLAS

CREATE TABLE USUARIOS (
    id_usuario        INT NOT NULL AUTO_INCREMENT,
    username          VARCHAR(50) NOT NULL,
    email_usuario     VARCHAR(100) NOT NULL,
    password_usuario  VARCHAR(255) NOT NULL,
    fecha_alta        DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    tokens            INT DEFAULT 0,
    rol               VARCHAR(50) NOT NULL,
    imagen_usuario    VARCHAR(150),
    
    CONSTRAINT pk_USUARIOS PRIMARY KEY (id_usuario),
    CONSTRAINT uq_email UNIQUE (email_usuario),    
    CONSTRAINT cb_rol CHECK (rol IN ('ALUMNO', 'PROFESOR', 'ADMINISTRADOR'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE MODULOS (
    codigo_modulo      VARCHAR(50) NOT NULL,
    nombre_asignatura  VARCHAR(100) NOT NULL,
    curso_modulo       VARCHAR(50) NOT NULL,
    
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
    id_usuario           INT,
    codigo_modulo        VARCHAR(50) NOT NULL,
    imagen_post          VARCHAR(150),
    
    CONSTRAINT pk_POSTS PRIMARY KEY (id_post),
    CONSTRAINT fk_POSTS_USUARIOS FOREIGN KEY (id_usuario) 
        REFERENCES USUARIOS (id_usuario) ON DELETE SET NULL,
    CONSTRAINT fk_POSTS_MODULOS FOREIGN KEY (codigo_modulo) 
        REFERENCES MODULOS (codigo_modulo) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE RESPUESTAS (
    id_respuesta         INT NOT NULL AUTO_INCREMENT,
    contenido_respuesta  TEXT NOT NULL,
    fecha_respuesta      DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id_post              INT NOT NULL,
    id_usuario           INT,
    es_mejor_respuesta   BOOLEAN DEFAULT FALSE NOT NULL,
    imagen_respuesta     VARCHAR(150),
    
    CONSTRAINT pk_RESPUESTAS PRIMARY KEY (id_respuesta),
    CONSTRAINT fk_RESPUESTAS_POSTS FOREIGN KEY (id_post) 
        REFERENCES POSTS (id_post) ON DELETE CASCADE,
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


-- 3. INSERCIÓN DE DATOS DE PRUEBA
INSERT INTO USUARIOS (username, email_usuario, password_usuario, rol) VALUES
('hpotter', 'potter@pixys.com', 'hp123', 'ALUMNO'),
('hgranger', 'granger@pixys.com', 'hg777', 'ALUMNO'),
('ssnape', 'snape@pixys.com', 'profe456', 'PROFESOR');

INSERT INTO MODULOS (codigo_modulo, nombre_asignatura, curso_modulo) VALUES
('MOD-BBDD', 'Bases de Datos Avanzadas', '1º DAW'),
('MOD-PROG', 'Programación', '1º DAW');

INSERT INTO MATRICULAS (id_usuario, codigo_modulo, fecha_inicio, fecha_final) VALUES
(1, 'MOD-BBDD', '2026-09-01', '2027-06-30'),
(2, 'MOD-BBDD', '2026-09-01', '2027-06-30');

INSERT INTO POSTS (titulo_post, contenido_post, id_usuario, codigo_modulo) VALUES
('Duda Joins', '¿Diferencia entre Inner y Left?', 1, 'MOD-BBDD');

INSERT INTO RESPUESTAS (contenido_respuesta, id_post, id_usuario, es_mejor_respuesta) VALUES
('El Inner solo trae coincidencias...', 1, 2, TRUE);

INSERT INTO HISTORICO_TOKENS (tokens, motivo, trimestre, id_usuario) VALUES
(20, 'MEJOR_RESPUESTA', '2026_T1', 2);
