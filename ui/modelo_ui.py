import tkinter as tk
from tkinter import ttk, messagebox
from controllers.modelo_controller import ModeloController
from controllers.marca_controller import MarcaController
from DB.database import DB

class ModeloUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ModeloController()
        self.marca_controller = MarcaController()

        tk.Label(self, text="Marca:").grid(row=0, column=0, padx=5, pady=5)

        # Combobox para seleccionar la marca directamente
        self.marca_var = tk.StringVar()
        self.marca_combo = ttk.Combobox(self, textvariable=self.marca_var, state="readonly")
        self.marca_combo.grid(row=0, column=1, padx=5, pady=5)
        self.cargar_marcas()

        tk.Label(self, text="Nombre del Modelo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Agregar Modelo", command=self.agregar_modelo).grid(row=2, column=0, columnspan=2, pady=5)

        self.lista_modelos = tk.Listbox(self, width=60)
        self.lista_modelos.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.lista_modelos.bind("<<ListboxSelect>>", self.cargar_seleccion)

        tk.Button(self, text="Eliminar Seleccionado", command=self.eliminar_modelo).grid(row=4, column=0, pady=5)
        tk.Button(self, text="Editar", command=self.editar_modelo).grid(row=4, column=1, pady=5)

        self.actualizar_lista()
        self.pack(fill=tk.BOTH, expand=True)

    def cargar_marcas(self):
        marcas = self.marca_controller.obtener_marcas()
        self.marcas_dict = {marca.nombre: marca.id_marca for marca in marcas}
        self.marca_combo['values'] = list(self.marcas_dict.keys())

    def actualizar_lista(self):
        self.lista_modelos.delete(0, tk.END)
        self.modelos = self.controller.obtener_modelos()

        if not self.modelos:
            messagebox.showerror("Error", "No se encontraron modelos. Verifica la conexión.")
            return

        self.modelos_dict = {modelo.id_modelo: modelo for modelo in self.modelos}

        for modelo in self.modelos:
            nombre_marca = next((nombre for nombre, id_marca in self.marcas_dict.items() if id_marca == modelo.id_marca), "Desconocido")
            self.lista_modelos.insert(tk.END, f"{modelo.id_modelo}: {nombre_marca} - {modelo.nombre_modelo}")

    def cargar_seleccion(self, event):
        seleccion = self.lista_modelos.curselection()
        if seleccion:
            index = seleccion[0]
            texto_modelo = self.lista_modelos.get(index)
            id_modelo = int(texto_modelo.split(":")[0])
            modelo = self.modelos_dict.get(id_modelo)

            if modelo:
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, modelo.nombre_modelo)

                for nombre, id_marca in self.marcas_dict.items():
                    if id_marca == modelo.id_marca:
                        self.marca_combo.set(nombre)

                self.modelo_seleccionado_id = modelo.id_modelo
            else:
                self.modelo_seleccionado_id = None

    def agregar_modelo(self):
        nombre_marca = self.marca_var.get()
        nombre_modelo = self.entry_nombre.get()

        if not nombre_marca or not nombre_modelo:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        id_marca = self.marcas_dict.get(nombre_marca)
        self.controller.agregar_modelo(id_marca, nombre_modelo)
        self.actualizar_lista()
        self.limpiar_formulario()

    def editar_modelo(self):
        if not hasattr(self, 'modelo_seleccionado_id') or self.modelo_seleccionado_id is None:
            messagebox.showwarning("Selección", "Debes seleccionar un modelo para editar.")
            return

        nuevo_nombre = self.entry_nombre.get()
        nueva_marca = self.marca_var.get()

        if not nuevo_nombre or not nueva_marca:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        id_marca_nueva = self.marcas_dict.get(nueva_marca)

        modelo = self.modelos_dict.get(self.modelo_seleccionado_id)
        if not modelo:
            messagebox.showerror("Error", "El modelo seleccionado no se pudo cargar correctamente.")
            return

        if nuevo_nombre == modelo.nombre_modelo and id_marca_nueva == modelo.id_marca:
            messagebox.showinfo("Sin Cambios", "No se realizaron cambios en el modelo.")
            return

        self.controller.actualizar_modelo(modelo.id_modelo, nuevo_nombre, id_marca_nueva)
        self.actualizar_lista()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Modelo actualizado correctamente.")

    def eliminar_modelo(self):
        seleccion = self.lista_modelos.curselection()
        if seleccion:
            index = seleccion[0]
            texto_modelo = self.lista_modelos.get(index)
            id_modelo = int(texto_modelo.split(":")[0])
            self.controller.eliminar_modelo(id_modelo)
            self.actualizar_lista()

    def cerrar_conexion(self):
        DB().close()
        print("🔒 Conexión cerrada correctamente.")

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.marca_combo.set("")
        self.modelo_seleccionado_id = None
