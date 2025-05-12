import tkinter as tk
from tkinter import messagebox, ttk
from controllers.servicio_controller import ServicioController
from controllers.refaccion_controller import RefaccionController

class ServicioUI:
    def __init__(self, root):
        self.root = root
        self.controller = ServicioController()
        self.refaccion_controller = RefaccionController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Gestión de Servicios", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Campos de Entrada
        tk.Label(self.frame, text="ID Vehículo:").grid(row=1, column=0)
        self.entry_id_vehiculo = tk.Entry(self.frame)
        self.entry_id_vehiculo.grid(row=1, column=1)

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

        # Lista de Refacciones
        self.tree_refacciones = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Cantidad"), show="headings")
        for col in self.tree_refacciones["columns"]:
            self.tree_refacciones.heading(col, text=col)
            self.tree_refacciones.column(col, width=100)
        self.tree_refacciones.grid(row=5, column=0, columnspan=4)

        self.refacciones_seleccionadas = []
        self.cargar_refacciones()

    def cargar_refacciones(self):
        self.refaccion_combo["values"] = [f"{ref.id_refaccion} - {ref.nombre}" for ref in self.refaccion_controller.obtener_refacciones()]

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

    def obtener_refacciones_seleccionadas(self):
        return self.refacciones_seleccionadas
    
    def destroy(self):
     self.frame.destroy()

