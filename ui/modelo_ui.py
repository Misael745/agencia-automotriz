import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.modelo_controller import ModeloController

class ModeloUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ModeloController()

        tk.Label(self, text="ID Marca:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_marca = tk.Entry(self)
        self.entry_id_marca.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Nombre del Modelo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Agregar Modelo", command=self.agregar_modelo).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Actualizar Lista", command=self.actualizar_lista).grid(row=3, column=0, columnspan=2, pady=5)

        self.lista_modelos = tk.Listbox(self, width=60)
        self.lista_modelos.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.lista_modelos.bind('<Double-1>', self.editar_modelo)

        tk.Button(self, text="Eliminar Seleccionado", command=self.eliminar_modelo).grid(row=5, column=0, columnspan=2)

        self.actualizar_lista()
        self.pack(fill=tk.BOTH, expand=True)  # Necesario para que se vea en el frame container

    def agregar_modelo(self):
        id_marca = self.entry_id_marca.get()
        nombre = self.entry_nombre.get()

        if not id_marca or not nombre:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        try:
            id_marca = int(id_marca)
            self.controller.agregar_modelo(id_marca, nombre)
            self.entry_id_marca.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.actualizar_lista()
        except ValueError:
            messagebox.showerror("Error", "El ID de la marca debe ser un número.")

    def actualizar_lista(self):
        self.lista_modelos.delete(0, tk.END)
        self.modelos = self.controller.obtener_modelos()
        for modelo in self.modelos:
            self.lista_modelos.insert(tk.END, f"{modelo.id_modelo}: Marca {modelo.id_marca} - {modelo.nombre_modelo}")

    def eliminar_modelo(self):
        seleccion = self.lista_modelos.curselection()
        if seleccion:
            index = seleccion[0]
            id_modelo = self.modelos[index].id_modelo
            confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este modelo?")
            if confirmar:
                self.controller.eliminar_modelo(id_modelo)
                self.actualizar_lista()

    def editar_modelo(self, event):
        seleccion = self.lista_modelos.curselection()
        if seleccion:
            index = seleccion[0]
            modelo = self.modelos[index]
            nuevo_nombre = simpledialog.askstring("Editar Modelo", "Nuevo nombre del modelo:", initialvalue=modelo.nombre_modelo)
            if nuevo_nombre:
                self.controller.actualizar_modelo(modelo.id_modelo, nuevo_nombre)
                self.actualizar_lista()
