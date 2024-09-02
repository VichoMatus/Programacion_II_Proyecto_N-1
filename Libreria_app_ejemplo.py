import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import re
from libro import Libro
from biblioteca import Biblioteca
from CTkMessagebox import CTkMessagebox

# Configuración del estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class VentanaBiblioteca(ctk.CTk):
    def __init__(self, biblioteca):
        super().__init__()

        # Configuración de la ventana principal
        self.biblioteca = biblioteca
        self.title("Sistema de Biblioteca")
        self.geometry("800x600")

        # Crear el frame superior
        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear el frame inferior
        self.frame_inferior = ctk.CTkFrame(self)
        self.frame_inferior.pack(fill="both", expand=True, padx=20, pady=10)

        # Campo de entrada para el nombre del libro
        self.entry_nombre = ctk.CTkEntry(self.frame_superior, placeholder_text="Nombre del libro")
        self.entry_nombre.pack(pady=10)

        # Campo de entrada para el autor del libro
        self.entry_autor = ctk.CTkEntry(self.frame_superior, placeholder_text="Nombre del autor")
        self.entry_autor.pack(pady=10)

        # Campo de entrada para la categoría del libro
        self.entry_categoria = ctk.CTkEntry(self.frame_superior, placeholder_text="Categoría del libro")
        self.entry_categoria.pack(pady=10)

        # Campo de entrada para la cantidad del libro
        self.entry_cantidad = ctk.CTkEntry(self.frame_superior, placeholder_text="Cantidad")
        self.entry_cantidad.pack(pady=10)

        # Botón para agregar el libro
        self.boton_agregar = ctk.CTkButton(self.frame_superior, text="Agregar Libro", command=self.agregar_libro)
        self.boton_agregar.pack(pady=5)

        # Botón para eliminar el libro seleccionado
        self.boton_eliminar = ctk.CTkButton(self.frame_superior, text="Eliminar Libro Seleccionado", command=self.eliminar_libro)
        self.boton_eliminar.pack(pady=5)

        # Treeview para mostrar los libros
        self.treeview = ttk.Treeview(self.frame_inferior, columns=("nombre", "autor", "categoria", "cantidad"), show="headings", height=8)

        self.treeview.column("nombre", anchor=tk.W, width=150)
        self.treeview.column("autor", anchor=tk.W, width=150)
        self.treeview.column("categoria", anchor=tk.W, width=150)
        self.treeview.column("cantidad", anchor=tk.W, width=100)

        self.treeview.heading("nombre", text="Nombre del Libro")
        self.treeview.heading("autor", text="Autor")
        self.treeview.heading("categoria", text="Categoría")
        self.treeview.heading("cantidad", text="Cantidad")

        self.treeview.pack(fill="both", expand=True, pady=20)
        
    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
        
    def agregar_libro(self):
        # Recoger los datos de los campos de entrada
        nombre = self.entry_nombre.get()
        autor = self.entry_autor.get()
        categoria = self.entry_categoria.get()
        cantidad_texto = self.entry_cantidad.get()

        if not cantidad_texto.isdigit():
            CTkMessagebox(title="Error", message="La cantidad debe ser un número.", icon="cancel")
            return

        cantidad = int(cantidad_texto)

        # Crear un objeto Libro y agregarlo a la biblioteca
        nuevo_libro = Libro(nombre, autor, categoria, cantidad)
        self.biblioteca.agregar_libro(nuevo_libro)

        # Agregar el libro al Treeview
        self.treeview.insert("", "end", values=(nombre, autor, categoria, cantidad))

        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)

    def eliminar_libro(self):
        # Obtener el elemento seleccionado en el Treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            CTkMessagebox(title="Advertencia", message="Seleccione un libro para eliminar.", icon="warning")
            return

        # Obtener el nombre del libro del Treeview
        nombre_libro = self.treeview.item(selected_item)["values"][0]

        # Eliminar el libro de la biblioteca
        self.biblioteca.eliminar_libro(nombre_libro)

        # Eliminar el libro del Treeview
        self.treeview.delete(selected_item)

        CTkMessagebox(title="Éxito", message=f"Libro '{nombre_libro}' eliminado correctamente.", icon="info")

if __name__ == "__main__":
    biblioteca = Biblioteca()
    app = VentanaBiblioteca(biblioteca)
    app.mainloop()



#metodo de ayuda para crear targetas con menus solicitados
def crear_tarjeta(self, menu):
    # Obtener el número de columnas y filas actuales
    num_tarjetas = len(self.menus_creados)
    fila = num_tarjetas // 2
    columna = num_tarjetas % 2

    # Crear la tarjeta con un tamaño fijo
    tarjeta = ctk.CTkFrame(tarjetas_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
    tarjeta.grid(row=fila, column=columna, padx=15, pady=15)

    # Hacer que la tarjeta sea completamente clickeable 
    tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

    # Cambiar el color del borde cuando el mouse pasa sobre la tarjeta
    tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))  # Cambia a rojo al pasar el mouse
    tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))  # Vuelve al verde al salir

    # Verifica si hay una imagen asociada con el menú
    if menu.icono_menu:
        # Crear y empaquetar el CTkLabel con la imagen, sin texto y con fondo transparente
        imagen_label = ctk.CTkLabel(tarjeta, image=menu.icono_menu, width=64, height=64, text="", bg_color="transparent")
        imagen_label.pack(anchor="center", pady=5, padx=10)
        imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en la imagen funcione

        # Agregar un Label debajo de la imagen para mostrar el nombre del menú
        texto_label = ctk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en el texto funcione

    else:
        print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")

#codigo de ayuda para desarrollar el evento que se debe gatillar, cuando se presiona cada targeta(Menu)
def tarjeta_click(self, event, menu):
        # Verificar si hay suficientes ingredientes en el stock para preparar el menú
        suficiente_stock = True
        if self.stock.lista_ingredientes==[]:
            suficiente_stock=False
        for ingrediente_necesario in menu.ingredientes:
            for ingrediente_stock in self.stock.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    if int(ingrediente_stock.cantidad) < int(ingrediente_necesario.cantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            # Descontar los ingredientes del stock
            for ingrediente_necesario in menu.ingredientes:
                for ingrediente_stock in self.stock.lista_ingredientes:
                    if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) - int(ingrediente_necesario.cantidad))
            
            # Agregar el menú al pedido
            self.pedido.agregar_menu(menu)
            
            # Actualizar el Treeview
            self.actualizar_treeview_pedido()

            # Actualizar el total del pedido
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            # Mostrar un mensaje indicando que no hay suficientes ingredientes usando CTkMessagebox
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")