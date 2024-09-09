class Libros_ejemplo:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.nombre} - Cantidad: {self.cantidad}"

    def actualizar_cantidad(self, cantidad):
        self.cantidad = cantidad
