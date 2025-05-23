
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.servicio_controller import ServicioController
from controllers.refaccion_controller import RefaccionController
from controllers.vehiculo_controller import VehiculoController

class ServicioUI:
    def __init__(self, root):
        self.root = root
        self.controller = ServicioController()
        self.refaccion_controller = RefaccionController()
        self.vehiculo_controller = VehiculoController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Gestión de Servicios", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Vehículos
        tk.Label(self.frame, text="Vehículo (Cliente):").grid(row=1, column=0)
        self.vehiculo_combo = ttk.Combobox(self.frame, state="readonly")
        self.vehiculo_combo.grid(row=1, column=1)

        # Descripción
        tk.Label(self.frame, text="Descripción:").grid(row=2, column=0)
        self.entry_descripcion = tk.Entry(self.frame)
        self.entry_descripcion.grid(row=2, column=1)

        # Refacciones
        tk.Label(self.frame, text="Refacción:").grid(row=3, column=0)
        self.refaccion_combo = ttk.Combobox(self.frame, state="readonly")
        self.refaccion_combo.grid(row=3, column=1)

        tk.Label(self.frame, text="Cantidad:").grid(row=3, column=2)
        self.entry_cantidad = tk.Entry(self.frame)
        self.entry_cantidad.grid(row=3, column=3)

        tk.Button(self.frame, text="Agregar Refacción", command=self.agregar_refaccion).grid(row=4, column=0, columnspan=4)

        # Tabla de refacciones
        self.tree_refacciones = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Cantidad"), show="headings")
        for col in self.tree_refacciones["columns"]:
            self.tree_refacciones.heading(col, text=col)
            self.tree_refacciones.column(col, width=100)
        self.tree_refacciones.grid(row=5, column=0, columnspan=4)

        # Botón final
        tk.Button(self.frame, text="Registrar Servicio", command=self.registrar_servicio).grid(row=6, column=0, columnspan=4, pady=10)

        self.refacciones_seleccionadas = []
        self.cargar_refacciones()
        self.cargar_vehiculos()

    def cargar_refacciones(self):
        self.refaccion_combo["values"] = [f"{ref.id_refaccion} - {ref.nombre}" for ref in self.refaccion_controller.obtener_refacciones()]

    def cargar_vehiculos(self):
        self.vehiculos = self.vehiculo_controller.obtener_vehiculos()
        self.vehiculo_combo["values"] = [f"{v.id_vehiculo} - {v.modelo} ({v.cliente})" for v in self.vehiculos]

    def agregar_refaccion(self):
        refaccion = self.refaccion_combo.get()
        cantidad = self.entry_cantidad.get()

        if not refaccion or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Selecciona una refacción y especifica una cantidad válida.")
            return

        ref_id = int(refaccion.split(" - ")[0])
        nombre = refaccion.split(" - ")[1]

        self.refacciones_seleccionadas.append((ref_id, nombre, int(cantidad)))
        self.tree_refacciones.insert("", "end", values=(ref_id, nombre, cantidad))

        self.entry_cantidad.delete(0, tk.END)

    def registrar_servicio(self):
        if not self.vehiculo_combo.get() or not self.entry_descripcion.get():
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return

        if not self.refacciones_seleccionadas:
            messagebox.showwarning("Validación", "Agrega al menos una refacción.")
            return

        vehiculo_id = int(self.vehiculo_combo.get().split(" - ")[0])
        descripcion = self.entry_descripcion.get()

        try:
            self.controller.agregar_servicio(vehiculo_id, descripcion, self.refacciones_seleccionadas)
            messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
            self.entry_descripcion.delete(0, tk.END)
            self.tree_refacciones.delete(*self.tree_refacciones.get_children())
            self.refacciones_seleccionadas.clear()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el servicio: {e}")

    def obtener_refacciones_seleccionadas(self):
        return self.refacciones_seleccionadas

    def destroy(self):
        self.frame.destroy()
