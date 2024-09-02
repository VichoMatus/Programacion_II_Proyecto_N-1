class Biblioteca:
    def __init__(self):
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)
        print(f"Libro '{libro.nombre}' agregado.")

    def eliminar_libro(self, nombre):
        libro_a_eliminar = None
        for libro in self.libros:
            if libro.nombre == nombre:
                libro_a_eliminar = libro
                break

        if libro_a_eliminar:
            self.libros.remove(libro_a_eliminar)
            print(f"Libro '{nombre}' eliminado.")
        else:
            print(f"No se encontró el libro '{nombre}'.")

    def listar_libros(self):
        if not self.libros:
            print("No hay libros en la biblioteca.")
        else:
            for libro in self.libros:
                print(libro)

