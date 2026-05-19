CREATE DATABASE abpTest;

-- Tabla de pruebas para demostración
CREATE TABLE IF NOT EXISTS pruebas (
    id_prueba INT AUTO_INCREMENT PRIMARY KEY,pruebas
    titulo VARCHAR(150) NOT NULL,
    descripcion VARCHAR(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos de ejemplo
INSERT INTO pruebas (titulo, descripcion) VALUES
('¿Cómo configurar Flask?', 'Necesito ayuda para configurar un proyecto Flask con SQLAlchemy'),
('Problema con TypeScript', 'No me compila el TypeScript, ¿alguien sabe qué está pasando?'),
('Dudas sobre la arquitectura', 'No entiendo bien la separación entre Repository y Service');