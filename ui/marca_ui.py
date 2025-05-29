import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.marca_controller import MarcaController

class MarcaUI:
    def __init__(self, root):
        self.root = root
        self.controller = MarcaController()

        # Frame principal con ttk
        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.crear_widgets()
        self.actualizar_lista()

    def crear_widgets(self):
        # Título
        ttk.Label(self.frame, text="Gestión de Marcas", font=("Arial", 16)).grid(row=0, column=0, pady=10, sticky="n")

        # Formulario
        form_frame = ttk.LabelFrame(self.frame, text="Agregar/Editar Marca", padding=10)
        form_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Nombre de la Marca:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_nombre = ttk.Entry(form_frame, width=30)
        self.entrada_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(form_frame, text="Agregar Marca", command=self.agregar_marca).grid(row=1, column=0, columnspan=2, pady=5)

        # Lista de marcas
        lista_frame = ttk.LabelFrame(self.frame, text="Marcas Registradas", padding=10)
        lista_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.frame.rowconfigure(2, weight=1)

        self.lista = tk.Listbox(lista_frame, height=10)
        self.lista.pack(side="left", fill="both", expand=True)
        self.lista.bind('<Double-1>', self.editar_marca)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.lista.yview)
        self.lista.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        botones_frame = ttk.Frame(self.frame)
        botones_frame.grid(row=3, column=0, pady=5)
        ttk.Button(botones_frame, text="Actualizar Lista", command=self.actualizar_lista).grid(row=0, column=0, padx=5)
        ttk.Button(botones_frame, text="Eliminar Seleccionado", command=self.eliminar_marca).grid(row=0, column=1, padx=5)

    def agregar_marca(self):
        nombre = self.entrada_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre de la marca no puede estar vacío.")
            return
        try:
            self.controller.agregar_marca(nombre)
            self.entrada_nombre.delete(0, tk.END)
            self.actualizar_lista()
            messagebox.showinfo("Éxito", "Marca agregada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la marca: {str(e)}")

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        try:
            self.marcas = self.controller.obtener_marcas()
            for marca in self.marcas:
                self.lista.insert(tk.END, f"{marca.id_marca}: {marca.nombre}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener marcas: {str(e)}")

    def eliminar_marca(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Selección", "Selecciona una marca para eliminar.")
            return
        index = seleccion[0]
        id_marca = self.marcas[index].id_marca
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta marca?")
        if confirmar:
            try:
                self.controller.eliminar_marca(id_marca)
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Marca eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la marca: {str(e)}")

    def editar_marca(self, event):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            marca = self.marcas[index]
            nuevo_nombre = simpledialog.askstring("Editar Marca", "Nuevo nombre:", initialvalue=marca.nombre)
            if nuevo_nombre:
                nuevo_nombre = nuevo_nombre.strip()
                if not nuevo_nombre:
                    messagebox.showwarning("Validación", "El nombre de la marca no puede estar vacío.")
                    return
                try:
                    self.controller.actualizar_marca(marca.id_marca, nuevo_nombre)
                    self.actualizar_lista()
                    messagebox.showinfo("Éxito", "Marca actualizada correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar la marca: {str(e)}")

    def destroy(self):
        self.frame.destroy()
