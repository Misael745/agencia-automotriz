import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from controllers.servicio_controller import ServicioController
from controllers.refaccion_controller import RefaccionController
from controllers.vehiculo_controller import VehiculoController

class ServicioUI:
    def __init__(self, root, volver_inicio_callback=None, cerrar_sesion_callback=None):
        self.root = root
        self.controller = ServicioController()
        self.refaccion_controller = RefaccionController()
        self.vehiculo_controller = VehiculoController()

        # Barra superior opcional
        if volver_inicio_callback or cerrar_sesion_callback:
            top_frame = tk.Frame(self.root, bg="#4682b4")
            top_frame.pack(fill="x")
            if volver_inicio_callback:
                tk.Button(top_frame, text="🏠 Inicio", bg="#f0f8ff", command=volver_inicio_callback).pack(side="left", padx=5, pady=5)
            if cerrar_sesion_callback:
                tk.Button(top_frame, text="🔒 Cerrar Sesión", bg="#f0f8ff", command=cerrar_sesion_callback).pack(side="right", padx=5, pady=5)

        self.frame = tk.Frame(self.root, bg="#f0f8ff")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Gestión de Servicios", font=("Arial", 18, "bold"), bg="#f0f8ff").grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self.frame, text="Vehículo (Cliente):", bg="#f0f8ff").grid(row=1, column=0, sticky="e")
        self.vehiculo_combo = ttk.Combobox(self.frame, state="readonly")
        self.vehiculo_combo.grid(row=1, column=1)
        tk.Label(self.frame, text="Descripción:", bg="#f0f8ff").grid(row=2, column=0, sticky="e")
        self.entry_descripcion = tk.Entry(self.frame, width=30)
        self.entry_descripcion.grid(row=2, column=1)
        tk.Label(self.frame, text="Próximo Servicio:", bg="#f0f8ff").grid(row=2, column=2, sticky="e")
        self.entry_fecha_proximo = DateEntry(self.frame, date_pattern='yyyy-mm-dd')
        self.entry_fecha_proximo.grid(row=2, column=3)

        tk.Label(self.frame, text="Refacción:", bg="#f0f8ff").grid(row=3, column=0, sticky="e")
        self.refaccion_combo = ttk.Combobox(self.frame, state="readonly")
        self.refaccion_combo.grid(row=3, column=1)
        tk.Label(self.frame, text="Cantidad:", bg="#f0f8ff").grid(row=3, column=2, sticky="e")
        self.entry_cantidad = tk.Entry(self.frame, width=10)
        self.entry_cantidad.grid(row=3, column=3)
        ttk.Button(self.frame, text="Agregar Refacción", command=self.agregar_refaccion).grid(row=4, column=0, columnspan=4, pady=5)

        self.tree_refacciones = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Cantidad"), show="headings")
        for col in self.tree_refacciones["columns"]:
            self.tree_refacciones.heading(col, text=col)
            self.tree_refacciones.column(col, width=120)
        self.tree_refacciones.grid(row=5, column=0, columnspan=4, pady=5)

        ttk.Button(self.frame, text="Registrar Servicio", command=self.registrar_servicio).grid(row=6, column=0, columnspan=4, pady=10)

        self.tree_servicios = ttk.Treeview(self.frame, columns=("ID", "Vehículo", "Descripción", "Fecha Prox", "Estatus"), show="headings")
        for col in self.tree_servicios["columns"]:
            self.tree_servicios.heading(col, text=col)
            self.tree_servicios.column(col, width=120)
        self.tree_servicios.grid(row=7, column=0, columnspan=4, pady=10)

        ttk.Button(self.frame, text="Cambiar Estatus", command=self.cambiar_estatus).grid(row=8, column=0, columnspan=4, pady=5)

        self.refacciones_seleccionadas = []
        self.cargar_vehiculos()
        self.cargar_refacciones()
        self.cargar_servicios()

    def cargar_vehiculos(self):
        vehiculos = self.vehiculo_controller.obtener_vehiculos()
        self.vehiculo_combo["values"] = [f"{v.id_vehiculo} - {v.modelo} ({v.cliente})" for v in vehiculos]

    def cargar_refacciones(self):
        self.refaccion_combo["values"] = [f"{r.id_refaccion} - {r.nombre}" for r in self.refaccion_controller.obtener_refacciones()]

    def agregar_refaccion(self):
        refaccion = self.refaccion_combo.get()
        cantidad = self.entry_cantidad.get()
        if not refaccion:
            messagebox.showerror("Error", "Selecciona una refacción.")
            return
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Especifica una cantidad válida (número positivo).")
            return

        ref_id = int(refaccion.split(" - ")[0])
        nombre = refaccion.split(" - ")[1]
        cantidad_solicitada = int(cantidad)

        refaccion_obj = self.refaccion_controller.obtener_refaccion_por_id(ref_id)
        if not refaccion_obj:
            messagebox.showerror("Error", f"No se encontró la refacción {nombre}.")
            return

        if refaccion_obj.cantidad < cantidad_solicitada:
            messagebox.showwarning("Cantidad Insuficiente",
                                   f"Solo hay {refaccion_obj.cantidad} unidades de {nombre} disponibles.")
            return

        self.refacciones_seleccionadas.append((ref_id, nombre, cantidad_solicitada))
        self.tree_refacciones.insert("", "end", values=(ref_id, nombre, cantidad_solicitada))

        # Limpiar campos
        self.refaccion_combo.set("")
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
        fecha_proximo = self.entry_fecha_proximo.get()
        self.controller.agregar_servicio(vehiculo_id, descripcion, self.refacciones_seleccionadas, fecha_proximo)
        messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
        self.entry_descripcion.delete(0, tk.END)
        self.tree_refacciones.delete(*self.tree_refacciones.get_children())
        self.refacciones_seleccionadas.clear()
        self.cargar_servicios()

    def cargar_servicios(self):
        self.tree_servicios.delete(*self.tree_servicios.get_children())
        servicios = self.controller.obtener_servicios()
        for s in servicios:
            self.tree_servicios.insert("", "end", values=(s.id_servicio, s.id_vehiculo, s.descripcion, s.fecha_proximo_servicio, s.estatus))

    def cambiar_estatus(self):
        selected = self.tree_servicios.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un servicio.")
            return
        id_servicio = self.tree_servicios.item(selected[0])["values"][0]
        ventana = tk.Toplevel(self.root)
        ventana.title("Cambiar Estatus")
        tk.Label(ventana, text="Nuevo Estatus:").pack(pady=5)
        estatus_var = tk.StringVar()
        estatus_combo = ttk.Combobox(ventana, textvariable=estatus_var, state="readonly", values=["En espera", "En proceso", "Finalizado"])
        estatus_combo.pack(pady=5)
        estatus_combo.set("En espera")
        def confirmar():
            nuevo = estatus_var.get()
            self.controller.cambiar_estatus(id_servicio, nuevo)
            messagebox.showinfo("Éxito", f"Estatus del servicio {id_servicio} cambiado a {nuevo}.")
            ventana.destroy()
            self.cargar_servicios()
        ttk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)

    def destroy(self):
        self.frame.destroy()