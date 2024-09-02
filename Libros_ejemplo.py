class Libro:
    def __init__(self, nombre, autor, categoria, cantidad):
        self.nombre = nombre
        self.autor = autor
        self.categoria = categoria
        self.cantidad = cantidad

    def __str__(self):
        return f"Nombre: {self.nombre}, Autor: {self.autor}, Categoría: {self.categoria}, Cantidad: {self.cantidad}"
