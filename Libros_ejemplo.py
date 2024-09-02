class Libros_ejemplo:
    def __init__(self, nombre, autor, categoria, cantidad):
        self.nombre = nombre
        self.autor = autor
        self.categoria = categoria
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.nombre} - {self.autor} - {self.categoria} - Cantidad: {self.cantidad}"
