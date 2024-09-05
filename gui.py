import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
from ingredientes import Stock
from pedido import Pedido, Menu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        self.stock = Stock()
        self.pedido = Pedido()

        # Pestañas
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        # Pestaña 1 - Ingreso de Ingredientes
        self.tab_ingreso = self.tabs.add("Ingreso de Ingredientes")
        self.crear_pestaña_ingreso()

        # Pestaña 2 - Pedido
        self.tab_pedido = self.tabs.add("Pedido")
        self.crear_pestaña_pedido()

    def crear_pestaña_ingreso(self):
        frame = ctk.CTkFrame(self.tab_ingreso)
        frame.pack(fill="both", expand=True)

        # Campos de entrada (alineados hacia la izquierda)
        self.entry_nombre = ctk.CTkEntry(frame, placeholder_text="Nombre del Ingrediente")
        self.entry_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_cantidad = ctk.CTkEntry(frame, placeholder_text="Cantidad")
        self.entry_cantidad.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Botón Ingresar (alineado hacia la izquierda)
        btn_ingresar = ctk.CTkButton(frame, text="Ingresar Ingrediente", command=self.ingresar_ingrediente)
        btn_ingresar.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Lista de ingredientes
        self.tree = ttk.Treeview(frame, columns=("Nombre", "Cantidad"), show="headings", height=10)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Botón Eliminar (colocado arriba de la tabla)
        btn_eliminar = ctk.CTkButton(frame, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        btn_eliminar.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        # Botón Generar Menú (colocado abajo)
        btn_generar_menu = ctk.CTkButton(frame, text="Generar Menú")
        btn_generar_menu.grid(row=3, column=1, columnspan=3, pady=10, sticky="ew")

    def crear_pestaña_pedido(self):
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True)

        # Menús disponibles (ejemplo con imágenes)
        self.imagen_papas = PhotoImage(file="icono_papas_fritas.png")  # Cargar imagen de papas fritas
        self.imagen_completo = PhotoImage(file="icono_hotdog.png")   # Cargar imagen de completo
        self.imagen_pepsi = PhotoImage(file="icono_cola.png")         # Cargar imagen de pepsi
        self.imagen_hamburguesa = PhotoImage(file="icono_hamburguesa.png")  # Cargar imagen de hamburguesa

        # Botones de Menús con imágenes
        self.btn_papas = ctk.CTkButton(frame, image=self.imagen_papas, text="Papas Fritas", command=lambda: self.agregar_menu("Papas Fritas"))
        self.btn_papas.grid(row=0, column=0, padx=10, pady=10)

        self.btn_completo = ctk.CTkButton(frame, image=self.imagen_completo, text="Completo", command=lambda: self.agregar_menu("Completo"))
        self.btn_completo.grid(row=0, column=1, padx=10, pady=10)

        self.btn_pepsi = ctk.CTkButton(frame, image=self.imagen_pepsi, text="Pepsi", command=lambda: self.agregar_menu("Pepsi"))
        self.btn_pepsi.grid(row=0, column=2, padx=10, pady=10)

        self.btn_hamburguesa = ctk.CTkButton(frame, image=self.imagen_hamburguesa, text="Hamburguesa", command=lambda: self.agregar_menu("Hamburguesa"))
        self.btn_hamburguesa.grid(row=0, column=3, padx=10, pady=10)

        # Tabla de pedido
        self.tree_pedido = ttk.Treeview(frame, columns=("Nombre del Menú", "Cantidad", "Precio Unitario"), show="headings")
        self.tree_pedido.heading("Nombre del Menú", text="Nombre del Menú")
        self.tree_pedido.heading("Cantidad", text="Cantidad")
        self.tree_pedido.heading("Precio Unitario", text="Precio Unitario")
        self.tree_pedido.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Total y botón de eliminar
        self.label_total = ctk.CTkLabel(frame, text="Total: $0.00")
        self.label_total.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_eliminar = ctk.CTkButton(frame, text="Eliminar Menú", command=self.eliminar_menu)
        self.btn_eliminar.grid(row=2, column=2, padx=10, pady=10)

        # Botón para generar boleta
        btn_boleta = ctk.CTkButton(frame, text="Generar Boleta", command=self.generar_boleta)
        btn_boleta.grid(row=2, column=3, padx=10, pady=10)

    def agregar_menu(self, nombre_menu):
        # Lógica para agregar un menú a la tabla de pedidos y actualizar el total
        pass

    def eliminar_menu(self):
        # Lógica para eliminar un menú seleccionado de la tabla de pedidos
        pass

    def generar_boleta(self):
        # Lógica para generar la boleta
        pass

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()

        # Permitir nombres con espacios
        if nombre.replace(" ", "").isalpha() and cantidad.isdigit():
            self.stock.agregar_ingrediente(nombre, int(cantidad))
            self.actualizar_treeview()
        else:
            messagebox.showwarning("Error", "Entrada inválida")


    def eliminar_ingrediente(self):
        selected_item = self.tree.selection()
        if selected_item:
            nombre = self.tree.item(selected_item, "values")[0]
            self.stock.eliminar_ingrediente(nombre)
            self.actualizar_treeview()

    def actualizar_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for nombre, cantidad in self.stock.mostrar_stock():
            self.tree.insert("", "end", values=(nombre, cantidad))

if __name__ == "__main__":
    app = App()
    app.mainloop()
