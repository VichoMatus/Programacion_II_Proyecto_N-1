import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
from ingredientes import Stock
from pedido import Pedido, Menu
from PIL import Image

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
        self.tab_ingreso = self.tabs.add("Pestaña 1")
        self.crear_pestaña_ingreso()

        # Pestaña 2 - Pedido
        self.tab_pedido = self.tabs.add("Pedido")
        self.crear_pestaña_pedido()

    def crear_pestaña_ingreso(self):
        # Dividir la pestaña en dos frames (izquierda para ingreso y derecha para visualización)
        frame_izquierda = ctk.CTkFrame(self.tab_ingreso)
        frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_derecha = ctk.CTkFrame(self.tab_ingreso)
        frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tab_ingreso.grid_columnconfigure(0, weight=1)
        self.tab_ingreso.grid_columnconfigure(1, weight=3)

        # Frame Izquierda - Ingreso de Ingredientes
        ingredientes_disponibles = ["Papas", "Vianesa", "Pan de Completo", "Tomate", "Palta", 
                                    "Pan de Hamburguesa", "Lámina de Queso", "Churrasco de Carne", "Bebida"]

        # Campo de selección de ingredientes
        self.combo_ingrediente = ttk.Combobox(frame_izquierda, values=ingredientes_disponibles, state="readonly")
        self.combo_ingrediente.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.combo_ingrediente.set("Seleccionar Ingrediente")

        # Campo para cantidad
        self.entry_cantidad = ctk.CTkEntry(frame_izquierda, placeholder_text="Cantidad")
        self.entry_cantidad.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Botón Ingresar
        btn_ingresar = ctk.CTkButton(frame_izquierda, text="Ingresar Ingrediente", command=self.ingresar_ingrediente)
        btn_ingresar.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Frame Derecha - Visualización de Ingredientes
        self.tree = ttk.Treeview(frame_derecha, columns=("Nombre", "Cantidad"), show="headings", height=15)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Botón Eliminar (debajo del Treeview)
        btn_eliminar = ctk.CTkButton(frame_derecha, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        btn_eliminar.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Botón Generar Menú
        btn_generar_menu = ctk.CTkButton(frame_derecha, text="Generar Menú")
        btn_generar_menu.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def crear_pestaña_pedido(self): 
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True)

        # Menús disponibles (ejemplo con imágenes)
        img_papas = Image.open("iconos/icono_papas_fritas.png")  # Cargar imagen de papas fritas
        img_completo = Image.open("iconos/icono_hotdog.png")   # Cargar imagen de completo
        img_pepsi = Image.open("iconos/icono_cola.png")         # Cargar imagen de pepsi
        img_hamburguesa = Image.open("iconos/icono_hamburguesa.png")  # Cargar imagen de hamburguesa


        self.imagen_papas = ctk.CTkImage(img_papas)  # Cargar imagen de papas fritas en ctk
        self.imagen_completo = ctk.CTkImage(img_completo)   # Cargar imagen de completo en ctk
        self.imagen_pepsi = ctk.CTkImage(img_pepsi)         # Cargar imagen de pepsi en ctk
        self.imagen_hamburguesa = ctk.CTkImage(img_hamburguesa)  # Cargar imagen de hamburguesa en ctk

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
        self.tree_pedido = ttk.Treeview(frame, columns=("Nombre del Menú", "Cantidad","Precio Unitario"), show="headings")
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

    def ingresar_ingrediente(self):
        nombre = self.combo_ingrediente.get()
        cantidad = self.entry_cantidad.get()

        if nombre == "Seleccionar Ingrediente":
            messagebox.showwarning("Error", "Por favor selecciona un ingrediente válido.")
            return

        if cantidad.isdigit():
            cantidad = int(cantidad)
            # Si el ingrediente ya existe en el stock, sumamos la cantidad
            if self.stock.ingrediente_existe(nombre):
                self.stock.agregar_ingrediente(nombre, cantidad)
            else:
                self.stock.agregar_ingrediente(nombre, cantidad)
            self.actualizar_treeview()
        else:
            messagebox.showwarning("Error", "Cantidad inválida")

    def eliminar_ingrediente(self):
        selected_item = self.tree.selection()
        if selected_item:
            nombre = self.tree.item(selected_item, "values")[0]
            self.stock.eliminar_ingrediente(nombre)
            self.actualizar_treeview()
        else:
            # Mostrar un mensaje de advertencia con un ícono
            messagebox.showwarning(
                "Advertencia",
                "No has seleccionado ningún ingrediente.",
                icon='warning'
            )

    def actualizar_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for nombre, cantidad in self.stock.mostrar_stock():
            self.tree.insert("", "end", values=(nombre, cantidad))
    def eliminar_menu(self):
        selected_item = self.tree_pedido.selection()
        if selected_item:
            self.tree_pedido.delete(selected_item)
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún menú.")
    def generar_boleta(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
