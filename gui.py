import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
from ingredientes import Stock
from pedido import Pedido, Menu
from PIL import Image
from fpdf import FPDF

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("900x700")
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
        frame_derecha.grid_rowconfigure(1, weight=1)  # Permite que el Treeview se expanda

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

        # Frame para botones en frame_derecha
        frame_botones = ctk.CTkFrame(frame_derecha)
        frame_botones.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configurar columnas del frame_botones para centrar el botón
        frame_botones.grid_columnconfigure(0, weight=0)
        frame_botones.grid_columnconfigure(1, weight=1)
        
        # Botón Eliminar (centrado en la parte superior del nuevo frame)
        btn_eliminar = ctk.CTkButton(frame_botones, text="Eliminar Ingrediente", command=self.eliminar_ingrediente, fg_color="black", text_color="White", width=30, height=30)
        btn_eliminar.grid(row=0, column=1, padx=10, pady=10)

        # Frame para Treeview y botón Generar Menú
        frame_pedido = ctk.CTkFrame(frame_derecha)
        frame_pedido.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Ocupa el espacio restante

        # Tabla de pedido en el frame de pedido
        self.tree = ttk.Treeview(frame_pedido, columns=("Nombre", "Cantidad"), show="headings", height=15)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Botón Generar Menú (en la parte inferior del frame_pedido)
        btn_generar_menu = ctk.CTkButton(frame_pedido, text="Generar Menú", width=200, height=40)
        btn_generar_menu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def crear_pestaña_pedido(self):
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True)

        # Crear dos CTkFrames, uno para los menús y otro para la tabla de pedidos
        frame_menus = ctk.CTkFrame(frame)
        frame_menus.pack(side="top", fill="x", padx=10, pady=10)

        frame_pedido = ctk.CTkFrame(frame)
        frame_pedido.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        img_papas = Image.open("iconos/icono_papas_fritas.png").resize((90, 90), Image.Resampling.LANCZOS)
        img_completo = Image.open("iconos/icono_hotdog.png").resize((90, 90), Image.Resampling.LANCZOS)
        img_pepsi = Image.open("iconos/icono_cola.png").resize((90, 90), Image.Resampling.LANCZOS)
        img_hamburguesa = Image.open("iconos/icono_hamburguesa.png").resize((90, 90), Image.Resampling.LANCZOS)

        # Crear objetos CTkImage con las imágenes redimensionadas
        self.imagen_papas = ctk.CTkImage(light_image=img_papas, size=(90, 90))
        self.imagen_completo = ctk.CTkImage(light_image=img_completo, size=(90, 90))
        self.imagen_pepsi = ctk.CTkImage(light_image=img_pepsi, size=(90, 90))
        self.imagen_hamburguesa = ctk.CTkImage(light_image=img_hamburguesa, size=(90, 90))

        # Botones de Menús con imágenes en el frame de menús
        self.btn_papas = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_papas, 
            width=90,    
            height=90,   
            text="Papas Fritas", 
            command=lambda: self.agregar_menu("Papas Fritas"), 
            fg_color="transparent",
            text_color="black",
            border_color="green",
            border_width=3,
            compound="top"
        )
        self.btn_papas.grid(row=0, column=0, padx=10, pady=10)

        # Evento para cambiar el borde a rojo cuando el ratón pasa sobre el botón
        self.btn_papas.bind("<Enter>", lambda e: self.btn_papas.configure(border_color="red"))
        # Evento para restaurar el borde original cuando el ratón sale del botón
        self.btn_papas.bind("<Leave>", lambda e: self.btn_papas.configure(border_color="green"))
        
        self.btn_pepsi = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_pepsi, 
            width=150, 
            height=150, 
            text="Pepsi", 
            command=lambda: self.agregar_menu("Pepsi"), 
            fg_color="transparent",
            text_color="black",
            border_color="green", 
            border_width=3,
            compound="top",
            hover_color="red"
        )
        self.btn_pepsi.grid(row=1, column=0, padx=10, pady=10)

        self.btn_hamburguesa = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_hamburguesa, 
            width=150, 
            height=150, 
            text="Hamburguesa", 
            command=lambda: self.agregar_menu("Hamburguesa"), 
            fg_color="transparent",
            text_color="black",
            border_color="green", 
            border_width=3,
            compound="top",
            hover_color="red"
        )
        self.btn_hamburguesa.grid(row=1, column=1, padx=10, pady=10)

        # Tabla de pedido en el frame de pedido
        self.tree_pedido = ttk.Treeview(frame_pedido, columns=("Nombre del Menú", "Cantidad", "Precio Unitario"), show="headings")
        self.tree_pedido.heading("Nombre del Menú", text="Nombre del Menú")
        self.tree_pedido.heading("Cantidad", text="Cantidad")
        self.tree_pedido.heading("Precio Unitario", text="Precio Unitario")
        self.tree_pedido.grid(row=1, column=4, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Total y botón de eliminar en el frame de pedido
        self.label_total = ctk.CTkLabel(frame_pedido, text="Total: $0.00")
        self.label_total.grid(row=0, column=6, pady=10)

        self.btn_eliminar = ctk.CTkButton(frame_pedido, text="Eliminar Menú", command=self.eliminar_menu)
        self.btn_eliminar.grid(row=0, column=7, padx=10, pady=10)

        # Botón para generar boleta en el frame de pedido
        btn_boleta = ctk.CTkButton(frame_pedido, text="Generar Boleta", command=self.generar_boleta)
        btn_boleta.grid(row=2, column=6, padx=10, pady=10)


    def agregar_menu(self, nombre_menu):
        # Diccionario de menús con sus precios e ingredientes
        menu_data = {
            "Papas Fritas": {"precio": 500, "ingredientes": {"Papas": 5}},
            "Pepsi": {"precio": 1100, "ingredientes": {"Bebida": 1}},
            "Completo": {"precio": 1800, "ingredientes": {"Vianesa": 1, "Pan de Completo": 1, "Tomate": 1, "Palta": 1}},
            "Hamburguesa": {"precio": 3500, "ingredientes": {"Pan de Hamburguesa": 1, "Lámina de Queso": 1, "Churrasco de Carne": 1}},
        }

        if nombre_menu in menu_data:
            menu_info = menu_data[nombre_menu]
            menu = Menu(nombre_menu, menu_info["precio"], menu_info["ingredientes"])

            # Verificar si hay suficiente stock y agregar el menú
            if self.pedido.agregar_menu(menu, self.stock):
                # Insertar en el Treeview
                self.tree_pedido.insert("", "end", values=(menu.nombre, 1, f"${menu.precio}"))
                self.actualizar_total()
            else:
                messagebox.showwarning("Advertencia", "No hay suficiente stock para este menú.")
    
    def actualizar_total(self):
        # Calcular y actualizar el total
        total = sum(menu.precio for menu in self.pedido.menus)
        self.label_total.configure(text=f"Total: ${total:.2f}")


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
        if not self.pedido.menus:
            messagebox.showwarning("Advertencia", "No hay menús en el pedido.")
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Boleta de Compra", ln=True, align="C")
            pdf.ln(10)

            pdf.cell(50, 10, txt="Nombre del Menú", border=1)
            pdf.cell(40, 10, txt="Cantidad", border=1)
            pdf.cell(50, 10, txt="Precio Unitario", border=1)
            pdf.cell(40, 10, txt="Total", border=1)
            pdf.ln(10)

            for menu in self.pedido.menus:
                print(f"Nombre: {menu.nombre}, Cantidad: {menu.cantidad}, Precio: {menu.precio}")  # Depuración
                pdf.cell(50, 10, txt=menu.nombre, border=1)
                pdf.cell(40, 10, txt=str(menu.cantidad), border=1)
                pdf.cell(50, 10, txt=f"${menu.precio:.2f}", border=1)
                pdf.cell(40, 10, txt=f"${menu.precio * menu.cantidad:.2f}", border=1)
                pdf.ln(10)

            pdf.ln(10)
            pdf.cell(50, 10, txt="Total a pagar:", ln=False)
            pdf.cell(40, 10, txt=f"${self.pedido.total:.2f}", ln=True)

            pdf.output("boleta.pdf")

            messagebox.showinfo("Éxito", "Boleta generada correctamente como boleta.pdf.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la boleta: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
