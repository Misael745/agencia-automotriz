import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController

class ClienteUI:
    def __init__(self, root):
        self.root = root  # Aquí root puede ser un Frame
        self.controller = ClienteController()
        self.cliente_seleccionado = None

        # Frame principal (dentro del root recibido, que puede ser un Frame)
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.crear_widgets()
        self.cargar_clientes()

    def crear_widgets(self):
        datos_frame = ttk.LabelFrame(self.frame, text="Datos del Cliente", padding=10)
        datos_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(datos_frame, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = ttk.Entry(datos_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(datos_frame, text="Apellido:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_apellido = ttk.Entry(datos_frame, width=30)
        self.entry_apellido.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(datos_frame, text="Teléfono:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_telefono = ttk.Entry(datos_frame, width=30)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(datos_frame, text="Correo:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_correo = ttk.Entry(datos_frame, width=30)
        self.entry_correo.grid(row=3, column=1, padx=5, pady=5)

        botones_frame = ttk.Frame(self.frame)
        botones_frame.grid(row=1, column=0, sticky="ew", pady=5)

        ttk.Button(botones_frame, text="Agregar", command=self.agregar_cliente).grid(row=0, column=0, padx=5)
        ttk.Button(botones_frame, text="Actualizar", command=self.actualizar_cliente).grid(row=0, column=1, padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar_cliente).grid(row=0, column=2, padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=3, padx=5)

        tabla_frame = ttk.LabelFrame(self.frame, text="Clientes Registrados", padding=10)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tabla_frame, columns=("ID", "Nombre", "Apellido", "Teléfono", "Correo"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def cargar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            clientes = self.controller.obtener_clientes()
            for cliente in clientes:
                self.tree.insert("", "end", values=cliente)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los clientes: {str(e)}")

    def agregar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        if not telefono.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe ser numérico.")
            return
        if correo and "@" not in correo:
            messagebox.showwarning("Validación", "El correo electrónico no es válido.")
            return

        try:
            success = self.controller.agregar_cliente(nombre, apellido, telefono, correo)
            if success:
                self.cargar_clientes()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el cliente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {str(e)}")

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
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return
        if not telefono.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe ser numérico.")
            return
        if correo and "@" not in correo:
            messagebox.showwarning("Validación", "El correo electrónico no es válido.")
            return

        try:
            self.controller.actualizar_cliente(self.cliente_seleccionado, nombre, apellido, telefono, correo)
            self.cargar_clientes()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el cliente?")
        if confirm:
            try:
                self.controller.eliminar_cliente(self.cliente_seleccionado)
                self.cargar_clientes()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.cliente_seleccionado = None
        self.tree.selection_remove(self.tree.selection())

    def destroy(self):
        self.frame.destroy()
