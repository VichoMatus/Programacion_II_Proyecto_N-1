import customtkinter as ctk
from tkinter import ttk
from Libros_ejemplo import Libros_ejemplo
from Biblioteca_ejemplo import Biblioteca_ejemplo
import re
<<<<<<< HEAD:Restaurante.py
from CTkMessagebox import CTkMessagebox

=======
import Ayuda_Codigo as AC
>>>>>>> origin/nmartinez:Libreria_app_ejemplo.py
class AplicacionConPestanas(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Gestion de Ingredientes y Pedido")
        self.geometry("1200x700")

        # Inicializar la Biblioteca
        self.biblioteca = Biblioteca_ejemplo()

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=600)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Ingredientes")
        self.tab2 = self.tabview.add("Eleccion de ProductosPedido")

        # Configurar el contenido de las pestañas
        self.configurar_pestana1()
        self.configurar_pestana2()

    def configurar_pestana1(self):
        # Dividir la pestaña en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        # Botón de ingreso
        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente", command=self.ingresar_libro)
        self.boton_ingresar.pack(pady=10)

        # Botón para eliminar libro arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=self.eliminar_libro)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre Ingrediente", "Cantidad"), show="headings")
        self.tree.heading("Nombre Ingrediente", text="Nombre Ingrediente")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def configurar_pestana2(self):
        # Dividir la pestaña en dos frames
        frame_Menu = ctk.CTkFrame(self.tab2)
        frame_Menu.pack(fill="both", expand=True, padx=10, pady=10)

        frame_precio = ctk.CTkFrame(self.tab2)
        frame_precio.pack(fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_Menu, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre_pestana2 = ctk.CTkEntry(frame_Menu)
        self.entry_nombre_pestana2.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_Menu, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad_pestana2 = ctk.CTkEntry(frame_Menu)
        self.entry_cantidad_pestana2.pack(pady=5)

        # Botón de ingreso
        self.boton_ingresar_pestana2 = ctk.CTkButton(frame_Menu, text="Ingresar Ingrediente", command=self.ingresar_libro_pestana2)
        self.boton_ingresar_pestana2.pack(pady=10)

    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        try:
            cantidad = int(cantidad)
            return cantidad > 0
        except ValueError:
            return False

    def ingresar_libro(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()

        # Validar entradas
        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        # Crear una instancia de el ingrediente
        libro = Libros_ejemplo(nombre, int(cantidad))

        # Agregar el libro a la biblioteca
        if self.biblioteca.agregar_libro(libro):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El Producto ya existe en la biblioteca.", icon="warning")

    def ingresar_libro_pestana2(self):
        nombre = self.entry_nombre_pestana2.get()
        cantidad = self.entry_cantidad_pestana2.get()

        # Validar entradas
        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        # Crear una instancia de el ingrediente
        libro = Libros_ejemplo(nombre, int(cantidad))

        # Agregar el libro a la biblioteca
        if self.biblioteca.agregar_libro(libro):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El Producto ya existe en la biblioteca.", icon="warning")

    def eliminar_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un Producto para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]

        # Eliminar el libro de la biblioteca
        if self.biblioteca.eliminar_libro(nombre):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El Producto no se pudo eliminar.", icon="warning")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los libros de la biblioteca al Treeview
        for libro in self.biblioteca.obtener_libros():
            self.tree.insert("", "end", values=(libro.nombre, libro.cantidad))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionConPestanas()
    app.mainloop()
