from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

# Aplicación de Biblioteca Personal con MongoDB y PyMongo


# Conexión con MongoDB

def crear_conexion():
    try:
        # Cambia esta cadena por tu conexión local o Atlas
        cadena_conexion = "mongodb://localhost:27017"

        cliente = MongoClient(cadena_conexion, serverSelectionTimeoutMS=3000)
        cliente.admin.command("ping")  # Probar conexión

        db = cliente["biblioteca_db"]
        return db["libros"]  # colección

    except ConnectionFailure:
        print("Error: No se pudo conectar a MongoDB. Revisa el servidor o la red.")
        exit()
    except ConfigurationError:
        print("Error en la cadena de conexión.")
        exit()
    except Exception as e:
        print(f"Falla inesperada al conectar: {e}")
        exit()

# Funciones CRUD

def agregar_libro(coleccion):
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado = input("Estado (Leído / No leído): ").strip()

    if estado not in ["Leído", "No leído"]:
        print("Estado inválido. Solo se permite 'Leído' o 'No leído'.\n")
        return

    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        coleccion.insert_one(libro)
        print("Libro agregado correctamente.\n")
    except Exception as e:
        print("Error al agregar libro:", e)


def actualizar_libro(coleccion):
    ver_libros(coleccion)
    id_titulo = input("Ingrese el título del libro a actualizar: ").strip()

    libro = coleccion.find_one({"titulo": id_titulo})
    if not libro:
        print("No se encontró un libro con ese título.\n")
        return

    nuevo_titulo = input("Nuevo título: ").strip()
    nuevo_autor = input("Nuevo autor: ").strip()
    nuevo_genero = input("Nuevo género: ").strip()
    nuevo_estado = input("Nuevo estado (Leído / No leído): ").strip()

    if nuevo_estado not in ["Leído", "No leído"]:
        print("Estado inválido.\n")
        return

    try:
        coleccion.update_one(
            {"_id": libro["_id"]},
            {
                "$set": {
                    "titulo": nuevo_titulo,
                    "autor": nuevo_autor,
                    "genero": nuevo_genero,
                    "estado": nuevo_estado
                }
            }
        )
        print("Libro actualizado exitosamente.\n")
    except Exception as e:
        print("Error al actualizar:", e)


def eliminar_libro(coleccion):
    ver_libros(coleccion)
    titulo = input("Ingrese el título del libro a eliminar: ").strip()

    libro = coleccion.find_one({"titulo": titulo})
    if not libro:
        print("No se encontró un libro con ese título.\n")
        return

    try:
        coleccion.delete_one({"_id": libro["_id"]})
        print("Libro eliminado.\n")
    except Exception as e:
        print("Error al eliminar libro:", e)


def ver_libros(coleccion):
    libros = list(coleccion.find())

    if not libros:
        print("No hay libros registrados.\n")
        return

    print("\nLISTADO DE LIBROS")
    print("-" * 60)
    for libro in libros:
        print(f"Título: {libro['titulo']} | Autor: {libro['autor']} | "
              f"Género: {libro['genero']} | Estado: {libro['estado']}")
    print("-" * 60 + "\n")


def buscar_libros(coleccion):
    campo = input("Buscar por (titulo/autor/genero): ").lower().strip()
    termino = input("Ingrese el término de búsqueda: ").strip()

    if campo not in ["titulo", "autor", "genero"]:
        print("Campo no válido.\n")
        return

    try:
        resultados = list(coleccion.find({campo: {"$regex": termino, "$options": "i"}}))

        if resultados:
            print("\nRESULTADOS DE BÚSQUEDA")
            print("-" * 60)
            for libro in resultados:
                print(f"Título: {libro['titulo']} | Autor: {libro['autor']} | "
                      f"Género: {libro['genero']} | Estado: {libro['estado']}")
            print("-" * 60 + "\n")
        else:
            print("No se encontraron coincidencias.\n")

    except Exception as e:
        print("Error en la búsqueda:", e)

# Menú principal

def menu():
    coleccion = crear_conexion()

    while True:
        print("========= MENÚ BIBLIOTECA PERSONAL =========")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        print("=============================================")

        opcion = input("Seleccione una opción (1-6): ").strip()
        print()

        if opcion == "1":
            agregar_libro(coleccion)
        elif opcion == "2":
            actualizar_libro(coleccion)
        elif opcion == "3":
            eliminar_libro(coleccion)
        elif opcion == "4":
            ver_libros(coleccion)
        elif opcion == "5":
            buscar_libros(coleccion)
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.\n")

# Ejecución principal

if __name__ == "__main__":
    menu()
