import tkinter as tk
from tkinter import messagebox, ttk
import re
from controllers.vehiculo_controller import VehiculoController
from controllers.modelo_controller import ModeloController
from controllers.cliente_controller import ClienteController

class VehiculoUI:
    def __init__(self, root):
        self.root = root
        self.controller = VehiculoController()
        self.modelo_controller = ModeloController()
        self.cliente_controller = ClienteController()

        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Gestión de Vehículos", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(self.frame, text="Modelo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_modelo = ttk.Combobox(self.frame, state="readonly", width=30)
        self.combo_modelo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Cliente:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_cliente = ttk.Combobox(self.frame, state="readonly", width=30)
        self.combo_cliente.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Año:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_anio = ttk.Entry(self.frame, width=30)
        self.entry_anio.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Placa:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_placa = ttk.Entry(self.frame, width=30)
        self.entry_placa.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        botones_frame = ttk.Frame(self.frame)
        botones_frame.grid(row=5, column=0, columnspan=4, pady=10)
        ttk.Button(botones_frame, text="Agregar", command=self.agregar_vehiculo).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Actualizar", command=self.actualizar_vehiculo).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar_vehiculo).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)

        lista_frame = ttk.LabelFrame(self.frame, text="Vehículos Registrados", padding=10)
        lista_frame.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)
        self.frame.rowconfigure(6, weight=1)

        self.tree = ttk.Treeview(lista_frame, columns=("ID", "Modelo", "Cliente", "Año", "Placa"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_vehiculo)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.cargar_modelos_clientes()
        self.cargar_vehiculos()

    def cargar_modelos_clientes(self):
        modelos = self.modelo_controller.obtener_modelos()
        self.combo_modelo["values"] = [m.nombre_modelo for m in modelos]
        self.modelos_dict = {m.nombre_modelo: m.id_modelo for m in modelos}

        clientes = self.cliente_controller.obtener_clientes()
        self.combo_cliente["values"] = [c[1] for c in clientes]
        self.clientes_dict = {c[1]: c[0] for c in clientes}

    def cargar_vehiculos(self):
        self.tree.delete(*self.tree.get_children())
        vehiculos = self.controller.obtener_vehiculos()
        for v in vehiculos:
            self.tree.insert("", "end", values=(v.id_vehiculo, v.modelo, v.cliente, v.anio, v.placa))

    def agregar_vehiculo(self):
        if not self.campos_validos():
            return

        modelo = self.combo_modelo.get()
        cliente = self.combo_cliente.get()
        modelo_id = self.modelos_dict.get(modelo)
        cliente_id = self.clientes_dict.get(cliente)

        if not modelo_id or not cliente_id:
            messagebox.showerror("Error", "Modelo o Cliente seleccionados no válidos.")
            return

        anio = self.entry_anio.get()
        placa = self.entry_placa.get().strip().upper()

        if self.placa_existente(placa):
            messagebox.showwarning("Duplicado", "Ya existe un vehículo con esa placa.")
            return

        self.controller.agregar_vehiculo(modelo_id, cliente_id, anio, placa)
        self.cargar_vehiculos()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")

    def actualizar_vehiculo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un vehículo para actualizar.")
            return

        vehiculo_id = self.tree.item(selected[0])['values'][0]
        modelo = self.combo_modelo.get()
        cliente = self.combo_cliente.get() or getattr(self, 'cliente_seleccionado_nombre', '')
        modelo_id = self.modelos_dict.get(modelo)
        cliente_id = self.clientes_dict.get(cliente)

        anio = self.entry_anio.get()
        placa = self.entry_placa.get().strip().upper()

        if not self.campos_validos():
            return

        if not modelo_id or not cliente_id:
            messagebox.showerror("Error", "No se puede actualizar: modelo o cliente no válidos.")
            return

        self.controller.actualizar_vehiculo(vehiculo_id, modelo_id, cliente_id, anio, placa)
        self.cargar_vehiculos()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Vehículo actualizado correctamente.")

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
            messagebox.showinfo("Éxito", "Vehículo eliminado correctamente.")

    def seleccionar_vehiculo(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.combo_modelo.set(values[1])
            self.combo_cliente.set(values[2])
            self.cliente_seleccionado_nombre = values[2]
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
        self.cliente_seleccionado_nombre = ''

    def campos_validos(self):
        if not self.combo_modelo.get() or not self.entry_anio.get() or not self.entry_placa.get():
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return False

        if not self.entry_anio.get().isdigit() or len(self.entry_anio.get()) != 4:
            messagebox.showwarning("Validación", "El año debe ser un número de 4 dígitos.")
            return False

        placa = self.entry_placa.get().strip().upper()
        if not re.match(r"^[A-Z0-9]{3}-[A-Z0-9]{4}$", placa):
            messagebox.showwarning("Validación", "Formato de placa inválido. Use formato similar a 2DF-355V.")
            return False
        return True

    def placa_existente(self, placa):
        for item in self.tree.get_children():
            valores = self.tree.item(item)["values"]
            if valores[4].strip().lower() == placa.strip().lower():
                return True
        return False

    def destroy(self):
        self.frame.destroy()
