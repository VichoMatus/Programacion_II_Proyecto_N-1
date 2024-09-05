class Menu:
    def __init__(self, nombre, precio, ingredientes_requeridos):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes_requeridos = ingredientes_requeridos  # Diccionario {ingrediente: cantidad}

class Pedido:
    def __init__(self):
        self.menus = []
        self.total = 0

    def agregar_menu(self, menu, stock):
        for ingrediente, cantidad in menu.ingredientes_requeridos.items():
            if not stock.verificar_stock(ingrediente, cantidad):
                return False  # No hay suficiente stock
        for ingrediente, cantidad in menu.ingredientes_requeridos.items():
            stock.ingredientes[ingrediente].reducir_cantidad(cantidad)
        self.menus.append(menu)
        self.total += menu.precio
        return True

    def eliminar_menu(self, menu, stock):
        if menu in self.menus:
            for ingrediente, cantidad in menu.ingredientes_requeridos.items():
                stock.ingredientes[ingrediente].agregar_cantidad(cantidad)
            self.menus.remove(menu)
            self.total -= menu.precio
