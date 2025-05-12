import tkinter as tk
from tkinter import messagebox, ttk
from controllers.refaccion_controller import RefaccionController

class RefaccionUI:
    def __init__(self, root):
        self.root = root
        self.controller = RefaccionController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Título
        tk.Label(self.frame, text="Gestión de Refacciones", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Entradas
        tk.Label(self.frame, text="Nombre:").grid(row=1, column=0)
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=1, column=1)

        tk.Label(self.frame, text="Descripción:").grid(row=2, column=0)
        self.entry_descripcion = tk.Entry(self.frame)
        self.entry_descripcion.grid(row=2, column=1)

        tk.Label(self.frame, text="Precio Unitario:").grid(row=3, column=0)
        self.entry_precio = tk.Entry(self.frame)
        self.entry_precio.grid(row=3, column=1)

        tk.Label(self.frame, text="Cantidad Disponible:").grid(row=4, column=0)
        self.entry_cantidad = tk.Entry(self.frame)
        self.entry_cantidad.grid(row=4, column=1)

        # Botones
        tk.Button(self.frame, text="Agregar", command=self.agregar_refaccion).grid(row=5, column=0)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar_refaccion).grid(row=5, column=1)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_refaccion).grid(row=5, column=2)

        # Tabla
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Descripción", "Precio", "Cantidad"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=3)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_refaccion)
        self.cargar_refacciones()

    def cargar_refacciones(self):
        self.tree.delete(*self.tree.get_children())
        refacciones = self.controller.obtener_refacciones()
        for ref in refacciones:
            self.tree.insert("", "end", values=(ref.id_refaccion, ref.nombre, ref.descripcion, ref.precio_unitario, ref.cantidad))

    def agregar_refaccion(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        try:
            precio = float(self.entry_precio.get())
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "El precio y la cantidad deben ser números.")
            return

        self.controller.agregar_refaccion(nombre, descripcion, precio, cantidad)
        self.cargar_refacciones()
        self.limpiar_formulario()

    def actualizar_refaccion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar una refacción")
            return

        ref_id = self.tree.item(selected[0])['values'][0]
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        try:
            precio = float(self.entry_precio.get())
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "El precio y la cantidad deben ser números.")
            return

        self.controller.actualizar_refaccion(ref_id, nombre, descripcion, precio, cantidad)
        self.cargar_refacciones()
        self.limpiar_formulario()

    def eliminar_refaccion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar una refacción")
            return

        ref_id = self.tree.item(selected[0])['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta refacción?")
        if confirmar:
            self.controller.eliminar_refaccion(ref_id)
            self.cargar_refacciones()
            self.limpiar_formulario()

    def seleccionar_refaccion(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, values[2])
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, values[3])
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, values[4])

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)

    def destroy(self):
     self.frame.destroy()
