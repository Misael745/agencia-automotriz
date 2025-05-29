import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.servicio_controller import ServicioController
from controllers.vehiculo_controller import VehiculoController
from controllers.refaccion_controller import RefaccionController
from datetime import date

class ServicioUI:
    def __init__(self, root):
        self.root = root
        self.controller = ServicioController()
        self.vehiculo_controller = VehiculoController()
        self.refaccion_controller = RefaccionController()

        self.frame = tk.Frame(self.root, bg="#f0f8ff")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Gestión de Servicios", font=("Arial", 18, "bold"), bg="#f0f8ff").grid(row=0, column=0, columnspan=7, pady=10)

        tk.Label(self.frame, text="Vehículo:", bg="#f0f8ff").grid(row=1, column=0)
        self.combo_vehiculo = ttk.Combobox(self.frame, state="readonly")
        self.combo_vehiculo.grid(row=1, column=1)

        tk.Label(self.frame, text="Descripción:", bg="#f0f8ff").grid(row=1, column=2)
        self.entry_descripcion = tk.Entry(self.frame)
        self.entry_descripcion.grid(row=1, column=3)

        tk.Label(self.frame, text="Fecha Próximo Servicio:", bg="#f0f8ff").grid(row=1, column=4)
        self.entry_fecha = DateEntry(self.frame, date_pattern='yyyy-mm-dd')
        self.entry_fecha.grid(row=1, column=5)

        tk.Label(self.frame, text="Estatus:", bg="#f0f8ff").grid(row=1, column=6)
        self.combo_estatus = ttk.Combobox(self.frame, values=["En espera", "En proceso", "Finalizado"], state="readonly")
        self.combo_estatus.grid(row=1, column=7)

        tk.Label(self.frame, text="Refacción:", bg="#f0f8ff").grid(row=2, column=0)
        self.combo_refaccion = ttk.Combobox(self.frame, state="readonly")
        self.combo_refaccion.grid(row=2, column=1)
        tk.Label(self.frame, text="Cantidad:", bg="#f0f8ff").grid(row=2, column=2)
        self.entry_cantidad = tk.Entry(self.frame)
        self.entry_cantidad.grid(row=2, column=3)
        self.lbl_stock = tk.Label(self.frame, text="Stock: ", bg="#f0f8ff")
        self.lbl_stock.grid(row=2, column=4)
        self.combo_refaccion.bind("<<ComboboxSelected>>", self.mostrar_stock)
        ttk.Button(self.frame, text="Agregar Refacción", command=self.agregar_refaccion).grid(row=2, column=5)

        self.tree_refacciones = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Cantidad"), show="headings")
        for col in self.tree_refacciones["columns"]:
            self.tree_refacciones.heading(col, text=col)
        self.tree_refacciones.grid(row=3, column=0, columnspan=8, pady=5)

        ttk.Button(self.frame, text="Registrar Servicio", command=self.registrar_servicio).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame, text="Actualizar Servicio", command=self.actualizar_servicio).grid(row=4, column=2, columnspan=2, pady=5)

        tk.Label(self.frame, text="Buscar por Cliente:", bg="#f0f8ff").grid(row=5, column=0)
        self.entry_cliente = tk.Entry(self.frame)
        self.entry_cliente.grid(row=5, column=1)
        ttk.Button(self.frame, text="Buscar", command=self.buscar_por_cliente).grid(row=5, column=2)
        ttk.Button(self.frame, text="Mostrar Todos", command=self.cargar_servicios).grid(row=5, column=3)

        self.tree_servicios = ttk.Treeview(self.frame, columns=("ID", "Vehículo", "Cliente", "Descripción", "Estatus", "Fecha Ingreso", "Fecha Próximo Servicio"), show="headings")
        for col in self.tree_servicios["columns"]:
            self.tree_servicios.heading(col, text=col)
            self.tree_servicios.column(col, width=120)
        self.tree_servicios.grid(row=6, column=0, columnspan=8, pady=10)
        self.tree_servicios.bind("<<TreeviewSelect>>", self.seleccionar_servicio)

        self.refacciones_seleccionadas = []
        self.cargar_vehiculos()
        self.cargar_refacciones()
        self.cargar_servicios()

    def cargar_vehiculos(self):
        vehiculos = self.vehiculo_controller.obtener_vehiculos()
        self.combo_vehiculo["values"] = [f"{v.id_vehiculo} - {v.modelo} ({v.cliente})" for v in vehiculos]
        self.vehiculos_dict = {f"{v.id_vehiculo} - {v.modelo} ({v.cliente})": v.id_vehiculo for v in vehiculos}

    def cargar_refacciones(self):
        self.refaccion_data = {f"{r.id_refaccion} - {r.nombre}": r for r in self.refaccion_controller.obtener_refacciones()}
        self.combo_refaccion["values"] = list(self.refaccion_data.keys())

    def mostrar_stock(self, event):
        seleccion = self.combo_refaccion.get()
        if seleccion in self.refaccion_data:
            stock = self.refaccion_data[seleccion].cantidad
            self.lbl_stock.config(text=f"Stock: {stock}")
        else:
            self.lbl_stock.config(text="Stock: N/A")

    def agregar_refaccion(self):
        refaccion = self.combo_refaccion.get()
        cantidad = self.entry_cantidad.get()
        if not refaccion or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showwarning("Aviso", "Selecciona refacción válida y cantidad.")
            return
        ref_id, nombre = refaccion.split(" - ")
        ref_id = int(ref_id)
        cantidad = int(cantidad)

        ref_obj = self.refaccion_controller.obtener_refaccion_por_id(ref_id)
        if not ref_obj:
            messagebox.showerror("Error", "Refacción no encontrada.")
            return

        cantidad_acumulada = cantidad
        for id_existente, _, cantidad_existente in self.refacciones_seleccionadas:
            if id_existente == ref_id:
                cantidad_acumulada += cantidad_existente
        if cantidad_acumulada > ref_obj.cantidad:
            messagebox.showwarning("Stock insuficiente", f"Solo hay {ref_obj.cantidad} disponibles en total. Ya tienes {cantidad_acumulada - cantidad} en la lista.")
            return

        for i, (id_existente, _, cantidad_existente) in enumerate(self.refacciones_seleccionadas):
            if id_existente == ref_id:
                self.refacciones_seleccionadas[i] = (ref_id, nombre, cantidad_existente + cantidad)
                self.actualizar_treeview()
                return

        self.refacciones_seleccionadas.append((ref_id, nombre, cantidad))
        self.actualizar_treeview()

    def actualizar_treeview(self):
        self.tree_refacciones.delete(*self.tree_refacciones.get_children())
        for ref_id, nombre, cantidad in self.refacciones_seleccionadas:
            self.tree_refacciones.insert("", "end", values=(ref_id, nombre, cantidad))

    def registrar_servicio(self):
        vehiculo = self.combo_vehiculo.get()
        descripcion = self.entry_descripcion.get()
        fecha = self.entry_fecha.get()
        if not vehiculo or not descripcion or not fecha or not self.refacciones_seleccionadas:
            messagebox.showwarning("Aviso", "Completa todos los campos y agrega al menos una refacción.")
            return
        id_vehiculo = self.vehiculos_dict[vehiculo]
        try:
            self.controller.agregar_servicio(id_vehiculo, descripcion, self.refacciones_seleccionadas, fecha)
            messagebox.showinfo("Éxito", "Servicio registrado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.refacciones_seleccionadas.clear()
        self.tree_refacciones.delete(*self.tree_refacciones.get_children())
        self.cargar_servicios()
        self.limpiar_campos()
    
    def limpiar_campos(self):
        self.combo_vehiculo.set("")
        self.entry_descripcion.delete(0, tk.END)
        self.entry_fecha.set_date(date.today())
        self.combo_estatus.set("")
        self.combo_refaccion.set("")
        self.entry_cantidad.delete(0, tk.END)
        self.lbl_stock.config(text="Stock: ")
        self.refacciones_seleccionadas.clear()
        self.tree_refacciones.delete(*self.tree_refacciones.get_children())

    def cargar_servicios(self):
        self.tree_servicios.delete(*self.tree_servicios.get_children())
        for s in self.controller.obtener_servicios():
            self.tree_servicios.insert("", "end", values=(s.id_servicio, s.placa, s.cliente, s.descripcion, s.estatus, s.fecha_ingreso, s.fecha_proximo_servicio))

    def seleccionar_servicio(self, event):
        selected = self.tree_servicios.selection()
        if selected:
            # Limpiar campos antes de cargar el nuevo servicio
            self.entry_descripcion.delete(0, tk.END)
            self.combo_estatus.set("")
            self.combo_vehiculo.set("")
            self.entry_fecha.set_date(date.today())

            # NO limpiar ni cargar la tabla de refacciones, ni modificar refacciones_seleccionadas

            values = self.tree_servicios.item(selected[0])["values"]
            if len(values) >= 7:
                self.entry_descripcion.insert(0, values[3])
                try:
                    if values[6]:
                        self.entry_fecha.set_date(values[6])
                except Exception:
                    messagebox.showerror("Error", f"Fecha inválida: {values[6]}")
                self.combo_estatus.set(values[4])


    def actualizar_servicio(self):
        selected = self.tree_servicios.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un servicio.")
            return
        servicio_id = self.tree_servicios.item(selected[0])["values"][0]
        descripcion = self.entry_descripcion.get()
        fecha = self.entry_fecha.get()
        estatus = self.combo_estatus.get()
        if not descripcion or not fecha or not estatus:
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return
        self.controller.actualizar_servicio(servicio_id, descripcion, fecha, estatus)
        messagebox.showinfo("Éxito", "Servicio actualizado correctamente.")
        self.cargar_servicios()
        self.limpiar_campos()

    def buscar_por_cliente(self):
        cliente = self.entry_cliente.get().strip()
        servicios = self.controller.obtener_servicios_por_cliente(cliente)
        self.tree_servicios.delete(*self.tree_servicios.get_children())
        for s in servicios:
            self.tree_servicios.insert("", "end", values=(s.id_servicio, s.placa, s.cliente, s.descripcion, s.estatus, s.fecha_ingreso, s.fecha_proximo_servicio))

    def destroy(self):
        self.frame.destroy()
