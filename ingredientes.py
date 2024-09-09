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
        self.ingredientes = {}  # Diccionario para almacenar ingredientes como objetos de la clase Ingrediente

    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre].agregar_cantidad(cantidad)
        else:
            self.ingredientes[nombre] = Ingrediente(nombre, cantidad)

    def ingrediente_existe(self, nombre):
        return nombre in self.ingredientes

    def eliminar_ingrediente(self, nombre):
        if nombre in self.ingredientes:
            del self.ingredientes[nombre]

    def mostrar_stock(self):
        return [(ingrediente.nombre, ingrediente.cantidad) for ingrediente in self.ingredientes.values()]

    def verificar_stock(self, nombre, cantidad):
        """ Verifica si hay suficiente stock del ingrediente """
        if nombre in self.ingredientes:
            return self.ingredientes[nombre].cantidad >= cantidad
        return False