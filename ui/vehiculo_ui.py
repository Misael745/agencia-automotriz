import tkinter as tk
from tkinter import messagebox, ttk
from controllers.vehiculo_controller import VehiculoController
from controllers.modelo_controller import ModeloController
from controllers.cliente_controller import ClienteController

class VehiculoUI:
    def __init__(self, root):
        self.root = root
        self.controller = VehiculoController()
        self.modelo_controller = ModeloController()
        self.cliente_controller = ClienteController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Título
        tk.Label(self.frame, text="Gestión de Vehículos", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Entradas
        tk.Label(self.frame, text="Modelo:").grid(row=1, column=0)
        self.combo_modelo = ttk.Combobox(self.frame, state="readonly")
        self.combo_modelo.grid(row=1, column=1)

        tk.Label(self.frame, text="Cliente:").grid(row=2, column=0)
        self.combo_cliente = ttk.Combobox(self.frame, state="readonly")
        self.combo_cliente.grid(row=2, column=1)

        tk.Label(self.frame, text="Año:").grid(row=3, column=0)
        self.entry_anio = tk.Entry(self.frame)
        self.entry_anio.grid(row=3, column=1)

        tk.Label(self.frame, text="Placa:").grid(row=4, column=0)
        self.entry_placa = tk.Entry(self.frame)
        self.entry_placa.grid(row=4, column=1)

        # Botones
        tk.Button(self.frame, text="Agregar", command=self.agregar_vehiculo).grid(row=5, column=0)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar_vehiculo).grid(row=5, column=1)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_vehiculo).grid(row=5, column=2)

        # Tabla
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Modelo", "Cliente", "Año", "Placa"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=3)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_vehiculo)

        self.cargar_modelos_clientes()
        self.cargar_vehiculos()

    def cargar_modelos_clientes(self):
        modelos = self.modelo_controller.obtener_modelos()
        self.combo_modelo["values"] = [f"{m.id_modelo} - {m.nombre_modelo}" for m in modelos]

        clientes = self.cliente_controller.obtener_clientes()
        self.combo_cliente["values"] = [f"{c.id_cliente} - {c.nombre}" for c in clientes]

    def cargar_vehiculos(self):
        self.tree.delete(*self.tree.get_children())
        vehiculos = self.controller.obtener_vehiculos()
        for v in vehiculos:
            self.tree.insert("", "end", values=(v.id_vehiculo, v.modelo, v.cliente, v.anio, v.placa))

    def agregar_vehiculo(self):
        modelo = self.combo_modelo.get().split(" - ")[0]
        cliente = self.combo_cliente.get().split(" - ")[0]
        anio = self.entry_anio.get()
        placa = self.entry_placa.get()

        self.controller.agregar_vehiculo(modelo, cliente, anio, placa)
        self.cargar_vehiculos()

    def actualizar_vehiculo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar un vehículo")
            return

        vehiculo_id = self.tree.item(selected[0])['values'][0]
        modelo = self.combo_modelo.get().split(" - ")[0]
        cliente = self.combo_cliente.get().split(" - ")[0]
        anio = self.entry_anio.get()
        placa = self.entry_placa.get()

        self.controller.actualizar_vehiculo(vehiculo_id, modelo, cliente, anio, placa)
        self.cargar_vehiculos()

    def eliminar_vehiculo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar un vehículo")
            return

        vehiculo_id = self.tree.item(selected[0])['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este vehículo?")
        if confirmar:
            self.controller.eliminar_vehiculo(vehiculo_id)
            self.cargar_vehiculos()
 
    def destroy(self):
        self.frame.destroy()