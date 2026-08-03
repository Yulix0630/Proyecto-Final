# practica_crud.py - Operaciones CRUD sobre la tabla contactos
import sqlite3

RUTA = "quantum_wallet.db"

def obtener_un_usuario_existente():
    """Busca un id_usuario válido de la tabla usuarios para evitar errores de FK."""
    con = sqlite3.connect(RUTA)
    cursor = con.cursor()
    cursor.execute("SELECT id_usuario FROM usuarios LIMIT 1;")
    fila = cursor.fetchone()
    con.close()
    if fila:
        return fila[0]
    return None

# C - CREATE
def crear_contactos(id_usuario):
    con = sqlite3.connect(RUTA)
    con.execute("PRAGMA foreign_keys = ON;")
    
    contactos = [
        ("Mama", "3001112233", id_usuario),
        ("Casa", "6041234567", id_usuario),
        ("Trabajo", "3109876543", id_usuario)
    ]
    
    con.executemany("INSERT INTO contactos (apodo, numero, id_usuario) VALUES (?, ?, ?);", contactos)
    con.commit()
    con.close()
    print(f"--- [CREATE] Contactos creados exitosamente para el usuario ID {id_usuario} ---")

# R - READ
def leer_contactos(id_usuario):
    con = sqlite3.connect(RUTA)
    filas = con.execute(
        "SELECT id_contacto, apodo, numero FROM contactos WHERE id_usuario = ?;", 
        (id_usuario,)
    ).fetchall()
    con.close()
    
    print(f"\n--- [READ] Lista de contactos para el usuario ID {id_usuario} ---")
    if not filas:
        print("No se encontraron contactos para este usuario.")
    for fila in filas:
        print(f"ID: {fila[0]} | Apodo: {fila[1]} | Número: {fila[2]}")
    return filas

# U - UPDATE
def actualizar_apodo(id_contacto, nuevo_apodo):
    con = sqlite3.connect(RUTA)
    con.execute("UPDATE contactos SET apodo = ? WHERE id_contacto = ?;", (nuevo_apodo, id_contacto))
    con.commit()
    con.close()
    print(f"\n--- [UPDATE] El contacto ID {id_contacto} se actualizó a '{nuevo_apodo}' ---")

# D - DELETE
def borrar_contacto(id_contacto):
    con = sqlite3.connect(RUTA)
    con.execute("DELETE FROM contactos WHERE id_contacto = ?;", (id_contacto,))
    con.commit()
    con.close()
    print(f"\n--- [DELETE] Se eliminó el contacto ID {id_contacto} ---")


# Bloque principal de ejecución secuencial
if __name__ == '__main__':
    # 1. Aseguramos que la base de datos tenga las tablas creadas
    import configurar_db
    configurar_db.crear_base_de_datos()

    # 2. Obtenemos un ID de usuario dinámico y seguro
    id_usuario_valido = obtener_un_usuario_existente()

    if id_usuario_valido:
        # 3. Ejecutamos CREATE con el usuario real
        crear_contactos(id_usuario_valido)

        # 4. Ejecutamos READ
        contactos_iniciales = leer_contactos(id_usuario_valido)

        # 5. Ejecutamos UPDATE sobre el primer contacto
        if contactos_iniciales:
            primer_id = contactos_iniciales[0][0]
            actualizar_apodo(primer_id, "Mama Celular Principal")
            leer_contactos(id_usuario_valido)

            # 6. Ejecutamos DELETE sobre el segundo contacto
            if len(contactos_iniciales) > 1:
                segundo_id = contactos_iniciales[1][0]
                borrar_contacto(segundo_id)
                leer_contactos(id_usuario_valido)
    else:
        print("Error: No existen usuarios en la base de datos para asignar contactos.")