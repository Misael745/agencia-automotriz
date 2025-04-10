import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController

class ClienteUI:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.controller = ClienteController()
        self.cliente_seleccionado = None

        self.crear_widgets()
        self.cargar_clientes()

    def crear_widgets(self):
        # Entradas
        tk.Label(self.frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(self.frame, text="Apellido:").grid(row=1, column=0, sticky="w")
        self.entry_apellido = tk.Entry(self.frame)
        self.entry_apellido.grid(row=1, column=1)

        tk.Label(self.frame, text="Teléfono:").grid(row=2, column=0, sticky="w")
        self.entry_telefono = tk.Entry(self.frame)
        self.entry_telefono.grid(row=2, column=1)

        tk.Label(self.frame, text="Correo:").grid(row=3, column=0, sticky="w")
        self.entry_correo = tk.Entry(self.frame)
        self.entry_correo.grid(row=3, column=1)

        # Botones
        tk.Button(self.frame, text="Agregar", command=self.agregar_cliente).grid(row=4, column=0, pady=10)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar_cliente).grid(row=4, column=1)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_cliente).grid(row=4, column=2)
        tk.Button(self.frame, text="Limpiar", command=self.limpiar_formulario).grid(row=4, column=3)

        # Tabla
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Apellido", "Teléfono", "Correo"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=5, column=0, columnspan=4, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    def cargar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        clientes = self.controller.obtener_clientes()
        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        telefono = self.entry_telefono.get()
        correo = self.entry_correo.get()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return

        success = self.controller.agregar_cliente(nombre, apellido, telefono, correo)
        if success:
            self.cargar_clientes()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")

    def seleccionar_cliente(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.cliente_seleccionado = values[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_apellido.delete(0, tk.END)
            self.entry_apellido.insert(0, values[2])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, values[3])
            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, values[4])

    def actualizar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente para actualizar.")
            return

        self.controller.actualizar_cliente(
            self.cliente_seleccionado,
            self.entry_nombre.get(),
            self.entry_apellido.get(),
            self.entry_telefono.get(),
            self.entry_correo.get()
        )
        self.cargar_clientes()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")

    def eliminar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente para eliminar.")
            return

        self.controller.eliminar_cliente(self.cliente_seleccionado)
        self.cargar_clientes()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.cliente_seleccionado = None
        self.tree.selection_remove(self.tree.selection())

    def destroy(self):
        self.frame.destroy()
