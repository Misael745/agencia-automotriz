import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.marca_controller import MarcaController

class MarcaUI:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.controller = MarcaController()

        self.entrada_nombre = tk.Entry(self.frame, width=40)
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.frame, text="Nombre de la Marca:").grid(row=0, column=0)

        tk.Button(self.frame, text="Agregar Marca", command=self.agregar_marca).grid(row=1, column=0, columnspan=2)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar_lista).grid(row=2, column=0, columnspan=2)

        self.lista = tk.Listbox(self.frame, width=60)
        self.lista.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.lista.bind('<Double-1>', self.editar_marca)

        tk.Button(self.frame, text="Eliminar Seleccionado", command=self.eliminar_marca).grid(row=4, column=0, columnspan=2)

        self.actualizar_lista()

    def agregar_marca(self):
        nombre = self.entrada_nombre.get()
        if nombre:
            self.controller.agregar_marca(nombre)
            self.entrada_nombre.delete(0, tk.END)
            self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        self.marcas = self.controller.obtener_marcas()
        for marca in self.marcas:
            self.lista.insert(tk.END, f"{marca.id_marca}: {marca.nombre}")

    def eliminar_marca(self):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            id_marca = self.marcas[index].id_marca
            self.controller.eliminar_marca(id_marca)
            self.actualizar_lista()

    def editar_marca(self, event):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            marca = self.marcas[index]
            nuevo_nombre = simpledialog.askstring("Editar Marca", "Nuevo nombre:", initialvalue=marca.nombre)
            if nuevo_nombre:
                self.controller.actualizar_marca(marca.id_marca, nuevo_nombre)
                self.actualizar_lista()

    def destroy(self):
        self.frame.destroy()
