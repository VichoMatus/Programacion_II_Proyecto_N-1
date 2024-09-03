import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import re
from CTkMessagebox import CTkMessagebox

# Configuración del estilo
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class Ventana_Restaurante(ctk.CTk):
    def __init__(self, biblioteca):
        super().__init__()

        # Configuración de la ventana principal
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

        # Agregar el libro al Treeview
        self.treeview.insert("", "end", values=(nombre, autor, categoria, cantidad))

        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)


if __name__ == "__main__":
    app = Ventana_Restaurante()
    app.mainloop()