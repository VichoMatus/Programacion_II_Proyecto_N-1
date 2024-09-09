class Menu:
    def __init__(self, nombre, precio, ingredientes_requeridos):
        self.nombre = nombre
        self.precio = precio
<<<<<<< Updated upstream
        self.ingredientes_requeridos = ingredientes_requeridos  # Diccionario {ingrediente: cantidad}
        self.cantidad = 1
        
=======
        self.ingredientes_requeridos = ingredientes_requeridos 
>>>>>>> Stashed changes

class Pedido:
    def __init__(self):
        self.menus = []
        self.total = 0
        self.ingredientes_usados = []  # Lista para rastrear ingredientes usados

    def agregar_menu(self, menu, stock):
        # Verificar si hay suficiente stock de cada ingrediente
        for ingrediente, cantidad in menu.ingredientes_requeridos.items():
            if not stock.verificar_stock(ingrediente, cantidad):
                return False  # No hay suficiente stock
        
        # Reducir el stock de los ingredientes usados
        for ingrediente, cantidad in menu.ingredientes_requeridos.items():
            stock.ingredientes[ingrediente].reducir_cantidad(cantidad)
        
        self.menus.append(menu)
        self.total += menu.precio
        # Guardar los ingredientes usados
        self.ingredientes_usados.append(menu.ingredientes_requeridos)
        return True

    def eliminar_menu(self, menu, stock):
        if menu in self.menus:
            # Restituir el stock de los ingredientes al eliminar el menÃº
            for ingrediente, cantidad in menu.ingredientes_requeridos.items():
                stock.ingredientes[ingrediente].agregar_cantidad(cantidad)
            
            self.menus.remove(menu)
            self.total -= menu.precio
            
            # Restablecer la cantidad de los ingredientes usados
            self.ingredientes_usados.remove(menu.ingredientes_requeridos)