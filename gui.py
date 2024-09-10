import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from ingredientes import Stock
from pedido import Pedido, Menu
from PIL import Image
from fpdf import FPDF
from datetime import datetime
from collections import defaultdict

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x700")
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

        # Frame para botones en frame_derecha
        frame_botones = ctk.CTkFrame(frame_derecha)
        frame_botones.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configurar columnas del frame_botones para centrar el botón
        frame_botones.grid_columnconfigure(0, weight=0)
        frame_botones.grid_columnconfigure(1, weight=1)
        
        # Botón Eliminar (centrado en la parte superior del nuevo frame)
        btn_eliminar = ctk.CTkButton(frame_botones, text="Eliminar Ingrediente", command=self.eliminar_ingrediente, fg_color="black", text_color="White", width=30, height=30)
        btn_eliminar.grid(row=0, column=1, padx=10, pady=10)
        
        # Frame Derecha - Visualización de Ingredientes
        self.tree = ttk.Treeview(frame_derecha, columns=("Nombre", "Cantidad"), show="headings", height=20)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Botón Generar Menú
        btn_generar_menu = ctk.CTkButton(frame_derecha, text="Generar Menú")
        btn_generar_menu.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def crear_pestaña_pedido(self): 
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True)

        # Crear dos CTkFrames, uno para los menús y otro para la tabla de pedidos
        frame_menus = ctk.CTkFrame(frame)
        frame_menus.pack(side="top", fill="x", padx=10, pady=10)

        frame_pedido = ctk.CTkFrame(frame)
        frame_pedido.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        img_papas = Image.open("iconos/icono_papas_fritas.png").resize((80, 80), Image.Resampling.LANCZOS)
        img_completo = Image.open("iconos/icono_hotdog.png").resize((80, 80), Image.Resampling.LANCZOS)
        img_pepsi = Image.open("iconos/icono_cola.png").resize((80, 80), Image.Resampling.LANCZOS)
        img_hamburguesa = Image.open("iconos/icono_hamburguesa.png").resize((80, 80), Image.Resampling.LANCZOS)

      

        self.imagen_papas = ctk.CTkImage(img_papas)
        self.imagen_completo = ctk.CTkImage(img_completo)
        self.imagen_pepsi = ctk.CTkImage(img_pepsi)
        self.imagen_hamburguesa = ctk.CTkImage(img_hamburguesa)

          # Crear objetos CTkImage con las imágenes redimensionadas
        self.imagen_papas = ctk.CTkImage(light_image=img_papas, size=(80, 80))
        self.imagen_completo = ctk.CTkImage(light_image=img_completo, size=(80, 80))
        self.imagen_pepsi = ctk.CTkImage(light_image=img_pepsi, size=(80, 80))
        self.imagen_hamburguesa = ctk.CTkImage(light_image=img_hamburguesa, size=(80, 80))

        #Botones de Menús con imágenes en el frame de menús
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

        self.btn_completo = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_completo, 
            width=90, 
            height=90,
            text="Completo", 
            command=lambda: self.agregar_menu("Completo"), 
            fg_color="transparent",
            text_color="black",
            border_color="green", 
            border_width=3,
            compound="top"
        )
        self.btn_completo.grid(row=0, column=1, padx=10, pady=10)

        self.btn_completo.bind("<Enter>", lambda e: self.btn_completo.configure(border_color="red"))
        self.btn_completo.bind("<Leave>", lambda e: self.btn_completo.configure(border_color="green"))

        self.btn_pepsi = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_pepsi, 
            width=90, 
            height=90, 
            text="Pepsi", 
            command=lambda: self.agregar_menu("Pepsi"), 
            fg_color="transparent",
            text_color="black",
            border_color="green", 
            border_width=3,
            compound="top"
        )
        self.btn_pepsi.grid(row=1, column=0, padx=10, pady=10)
        self.btn_pepsi.bind("<Enter>", lambda e: self.btn_pepsi.configure(border_color="red"))
        self.btn_pepsi.bind("<Leave>", lambda e: self.btn_pepsi.configure(border_color="green"))

        self.btn_hamburguesa = ctk.CTkButton(
            frame_menus, 
            image=self.imagen_hamburguesa, 
            width=90, 
            height=90, 
            text="Hamburguesa", 
            command=lambda: self.agregar_menu("Hamburguesa"), 
            fg_color="transparent",
            text_color="black",
            border_color="green", 
            border_width=3,
            compound="top"
        )
        self.btn_hamburguesa.grid(row=1, column=1, padx=10, pady=10)
        self.btn_hamburguesa.bind("<Enter>", lambda e: self.btn_hamburguesa.configure(border_color="red"))
        self.btn_hamburguesa.bind("<Leave>", lambda e: self.btn_hamburguesa.configure(border_color="green"))

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

    def actualizar_total(self):
        # Calcular y actualizar el total
        total = sum(menu.precio for menu in self.pedido.menus)
        self.label_total.configure(text=f"Total: ${total:.2f}")

    def agregar_menu(self, nombre_menu):
        menu_data = {
            "Papas Fritas": {"precio": 500, "ingredientes": {"Papas": 5}},
            "Pepsi": {"precio": 1100, "ingredientes": {"Bebida": 1}},
            "Completo": {"precio": 1800, "ingredientes": {"Vianesa": 1, "Pan de Completo": 1, "Tomate": 1, "Palta": 1}},
            "Hamburguesa": {"precio": 3500, "ingredientes": {"Pan de Hamburguesa": 1, "Lámina de Queso": 1, "Churrasco de Carne": 1}},
        }

        if nombre_menu in menu_data:
            menu_info = menu_data[nombre_menu]
            menu = Menu(nombre_menu, menu_info["precio"], menu_info["ingredientes"])

            if self.pedido.agregar_menu(menu, self.stock):
                # Verificar si el menú ya está en el Treeview
                item_exists = False
                for item in self.tree_pedido.get_children():
                    valores = self.tree_pedido.item(item, "values")
                    if valores[0] == nombre_menu:
                        # Si está, aumentar la cantidad
                        cantidad_actual = int(valores[1])
                        nueva_cantidad = cantidad_actual + 1
                        self.tree_pedido.item(item, values=(nombre_menu, nueva_cantidad, f"${menu.precio}"))
                        item_exists = True
                        break
                
                if not item_exists:
                    # Si no está, insertar una nueva fila
                    self.tree_pedido.insert("", "end", values=(menu.nombre, 1, f"${menu.precio}"))
                
                self.actualizar_total()
                # Actualizar la pestaña de ingredientes
                self.actualizar_treeview()
            else:
                messagebox.showwarning("Advertencia", "No hay suficiente stock para este menú.")



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
            valores = self.tree_pedido.item(selected_item, "values")
            nombre_menu = valores[0]
            cantidad_menu = int(valores[1])
            
            # Buscar el menú en el pedido
            menu_data = {
                "Papas Fritas": {"precio": 500, "ingredientes": {"Papas": 5}},
                "Pepsi": {"precio": 1100, "ingredientes": {"Bebida": 1}},
                "Completo": {"precio": 1800, "ingredientes": {"Vianesa": 1, "Pan de Completo": 1, "Tomate": 1, "Palta": 1}},
                "Hamburguesa": {"precio": 3500, "ingredientes": {"Pan de Hamburguesa": 1, "Lámina de Queso": 1, "Churrasco de Carne": 1}},
            }

            for _ in range(cantidad_menu):
                menu_info = menu_data.get(nombre_menu, {"ingredientes": {}})
                menu = Menu(nombre_menu, menu_info.get("precio", 0), menu_info["ingredientes"])
                self.pedido.eliminar_menu(menu, self.stock)
            
            self.tree_pedido.delete(selected_item)
            self.actualizar_total()
            # Actualizar la pestaña de ingredientes
            self.actualizar_treeview()
        else:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún menú.")

    def generar_boleta(self):
        if not self.pedido.menus:
            messagebox.showwarning("Advertencia", "No hay menús en el pedido.")
            return

        try:
            # Agrupar los productos por nombre y sumar las cantidades
            productos_agrupados = defaultdict(lambda: {'cantidad': 0, 'precio': 0})
            
            for menu in self.pedido.menus:
                productos_agrupados[menu.nombre]['cantidad'] += menu.cantidad
                productos_agrupados[menu.nombre]['precio'] = menu.precio  # Asumimos que el precio es el mismo por producto

            # Creación del PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Establecer fuente y tamaño
            pdf.set_font("Arial", size=12)

            # Encabezado de la boleta
            pdf.cell(200, 10, txt="Boleta Restaurante", ln=True, align="C")
            pdf.ln(5)

            # Información del negocio
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt="Universidad Catolica", ln=True)
            pdf.cell(200, 10, txt="RUT: 12345678-9", ln=True)
            pdf.cell(200, 10, txt="Dirección: Condominio Fundo del Carmen", ln=True)
            pdf.cell(200, 10, txt="Teléfono: +56 9 9879 7181", ln=True)

            # Fecha a la derecha
            pdf.set_xy(150, 50)  # Posiciona la fecha en la esquina derecha
            pdf.cell(50, 10, txt=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align="R")
            pdf.ln(10)

            # Encabezado de la tabla
            pdf.set_xy(10, 70)  # Posiciona la tabla debajo de la información del negocio y fecha
            pdf.set_font("Arial", "B", 12)
            pdf.cell(60, 10, txt="Nombre", border=1, align="C")
            pdf.cell(40, 10, txt="Cantidad", border=1, align="C")
            pdf.cell(45, 10, txt="Precio Unitario", border=1, align="C")
            pdf.cell(45, 10, txt="Subtotal", border=1, align="C")
            pdf.ln()

            # Contenido de la tabla
            pdf.set_font("Arial", size=12)
            total = 0
            for nombre, datos in productos_agrupados.items():
                cantidad = datos['cantidad']
                precio_unitario = datos['precio']
                subtotal = precio_unitario * cantidad
                total += subtotal

                pdf.cell(60, 10, txt=nombre, border=1)
                pdf.cell(40, 10, txt=str(cantidad), border=1, align="C")
                pdf.cell(45, 10, txt=f"${precio_unitario:.2f}", border=1, align="R")
                pdf.cell(45, 10, txt=f"${subtotal:.2f}", border=1, align="R")
                pdf.ln()

            # Subtotales y Totales
            pdf.ln(5)
            pdf.cell(145, 10, txt="Subtotal:", align="R")
            pdf.cell(45, 10, txt=f"${total:.2f}", align="R")
            pdf.ln()

            iva = total * 0.19
            pdf.cell(145, 10, txt="IVA (19%):", align="R")
            pdf.cell(45, 10, txt=f"${iva:.2f}", align="R")
            pdf.ln()

            total_final = total + iva
            pdf.cell(145, 10, txt="Total:", align="R")
            pdf.cell(45, 10, txt=f"${total_final:.2f}", align="R")
            pdf.ln(10)

            # Pie de página
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, txt="Gracias por su compra. Para cualquier consulta, llámenos al +56 9 1234 5678.", ln=True, align="C")
            pdf.cell(200, 10, txt="Los productos adquiridos no tienen garantía.", ln=True, align="C")

            # Guardar PDF
            pdf.output("boleta.pdf")

            messagebox.showinfo("Éxito", "Boleta generada correctamente como boleta.pdf.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la boleta: {str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()