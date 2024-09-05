class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def agregar_cantidad(self, cantidad):
        self.cantidad += cantidad

    def reducir_cantidad(self, cantidad):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
            return True
        else:
            return False

class Stock:
    def __init__(self):
        self.ingredientes = {}

    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre].agregar_cantidad(cantidad)
        else:
            self.ingredientes[nombre] = Ingrediente(nombre, cantidad)

    def eliminar_ingrediente(self, nombre):
        if nombre in self.ingredientes:
            del self.ingredientes[nombre]

    def verificar_stock(self, nombre, cantidad):
        if nombre in self.ingredientes and self.ingredientes[nombre].cantidad >= cantidad:
            return True
        else:
            return False

    def mostrar_stock(self):
        return [(i.nombre, i.cantidad) for i in self.ingredientes.values()]
