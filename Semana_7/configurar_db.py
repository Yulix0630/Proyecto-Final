# configurar_db.py - Crea quantum_wallet.db con SQLite
import sqlite3

def crear_base_de_datos():
    conexion = sqlite3.connect("quantum_wallet.db")
    cursor = conexion.cursor()
    
    # Habilitar soporte de llaves foráneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Tabla 1: usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre     TEXT NOT NULL,
        email      TEXT NOT NULL UNIQUE,
        nit        TEXT
    );
    """)

    # Tabla 2: wallets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        id_wallet      INTEGER PRIMARY KEY AUTOINCREMENT,
        saldo          REAL NOT NULL DEFAULT 0,
        id_propietario INTEGER NOT NULL,
        FOREIGN KEY (id_propietario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    """)

    # Tabla 3: contactos (Requerida para la Actividad 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contactos (
        id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
        apodo       TEXT NOT NULL,
        numero      TEXT NOT NULL,
        id_usuario  INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    """)

    # Limpieza previa para reinicio limpio
    cursor.execute("DELETE FROM contactos;")
    cursor.execute("DELETE FROM wallets;")
    cursor.execute("DELETE FROM usuarios;")

    # Inserciones iniciales de prueba (Carlos Molina y Guillermo Rios)
    cursor.execute("INSERT INTO usuarios (nombre, email, nit) VALUES (?, ?, ?);", 
                   ("Carlos Molina", "carlosmt67@gmail.com", None))
    id_carlos = cursor.lastrowid

    cursor.execute("INSERT INTO usuarios (nombre, email, nit) VALUES (?, ?, ?);", 
                   ("Guillermo Rios", "guillermo.rios@example.com", "7455989"))
    id_guillermo = cursor.lastrowid

    # Billeteras iniciales
    cursor.execute("INSERT INTO wallets (saldo, id_propietario) VALUES (?, ?);", (150000.50, id_carlos))
    cursor.execute("INSERT INTO wallets (saldo, id_propietario) VALUES (?, ?);", (5230000.00, id_guillermo))

    conexion.commit()
    conexion.close()
    print("Base de datos e infraestructura de tablas creadas: quantum_wallet.db")

if __name__ == '__main__':
    crear_base_de_datos()