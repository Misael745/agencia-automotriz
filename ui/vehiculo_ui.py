
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

        tk.Label(self.frame, text="Gestión de Vehículos", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

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

        tk.Button(self.frame, text="Agregar", command=self.agregar_vehiculo).grid(row=5, column=0)
        tk.Button(self.frame, text="Actualizar", command=self.actualizar_vehiculo).grid(row=5, column=1)
        tk.Button(self.frame, text="Eliminar", command=self.eliminar_vehiculo).grid(row=5, column=2)
        tk.Button(self.frame, text="Limpiar", command=self.limpiar_formulario).grid(row=5, column=3)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Modelo", "Cliente", "Año", "Placa"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=4)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_vehiculo)

        self.cargar_modelos_clientes()
        self.cargar_vehiculos()

    def cargar_modelos_clientes(self):
        modelos = self.modelo_controller.obtener_modelos()
        self.modelos_dict = {m.nombre_modelo: m.id_modelo for m in modelos}
        self.combo_modelo["values"] = list(self.modelos_dict.keys())

        clientes = self.cliente_controller.obtener_clientes()
        self.clientes_dict = {c[1]: c[0] for c in clientes}
        self.combo_cliente["values"] = list(self.clientes_dict.keys())

    def cargar_vehiculos(self):
        self.tree.delete(*self.tree.get_children())
        vehiculos = self.controller.obtener_vehiculos()
        for v in vehiculos:
            self.tree.insert("", "end", values=(v.id_vehiculo, v.modelo, v.cliente, v.anio, v.placa))

    def placa_existente(self, placa):
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores[4].strip().lower() == placa.strip().lower():
                return True
        return False

    def agregar_vehiculo(self):
        if not self.campos_validos():
            return

        modelo_id = self.modelos_dict.get(self.combo_modelo.get())
        cliente_id = self.clientes_dict.get(self.combo_cliente.get())
        anio = self.entry_anio.get()
        placa = self.entry_placa.get()

        if self.placa_existente(placa):
            messagebox.showwarning("Duplicado", "Ya existe un vehículo con esa placa.")
            return

        self.controller.agregar_vehiculo(modelo_id, cliente_id, anio, placa)
        self.cargar_vehiculos()
        self.limpiar_formulario()

    def actualizar_vehiculo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un vehículo para actualizar.")
            return

        if not self.campos_validos():
            return

        modelo_id = self.modelos_dict.get(self.combo_modelo.get())
        cliente_id = self.clientes_dict.get(self.combo_cliente.get())
        vehiculo_id = self.tree.item(selected[0])['values'][0]
        anio = self.entry_anio.get()
        placa = self.entry_placa.get()

        self.controller.actualizar_vehiculo(vehiculo_id, modelo_id, cliente_id, anio, placa)
        self.cargar_vehiculos()
        self.limpiar_formulario()

    def eliminar_vehiculo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un vehículo para eliminar.")
            return

        vehiculo_id = self.tree.item(selected[0])['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este vehículo?")
        if confirmar:
            self.controller.eliminar_vehiculo(vehiculo_id)
            self.cargar_vehiculos()
            self.limpiar_formulario()

    def seleccionar_vehiculo(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.combo_modelo.set(values[1])
            self.combo_cliente.set(values[2])
            self.entry_anio.delete(0, tk.END)
            self.entry_anio.insert(0, values[3])
            self.entry_placa.delete(0, tk.END)
            self.entry_placa.insert(0, values[4])

    def limpiar_formulario(self):
        self.combo_modelo.set("")
        self.combo_cliente.set("")
        self.entry_anio.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def campos_validos(self):
        modelo = self.combo_modelo.get()
        cliente = self.combo_cliente.get()
        anio = self.entry_anio.get()
        placa = self.entry_placa.get()

        if not modelo or not cliente or not anio or not placa:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return False

        if not anio.isdigit() or len(anio) != 4:
            messagebox.showwarning("Validación", "El año debe ser un número de 4 dígitos.")
            return False

        return True

    def destroy(self):
        self.frame.destroy()
