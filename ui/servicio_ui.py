import tkinter as tk
from tkinter import messagebox
from controllers.servicio_controller import ServicioController
from datetime import datetime

class ServicioUI:
    def __init__(self, root):
        self.root = root
        self.controller = ServicioController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="ID Vehículo:").grid(row=0, column=0)
        self.entry_id_vehiculo = tk.Entry(self.frame)
        self.entry_id_vehiculo.grid(row=0, column=1)

        tk.Label(self.frame, text="Descripción:").grid(row=1, column=0)
        self.entry_descripcion = tk.Entry(self.frame)
        self.entry_descripcion.grid(row=1, column=1)

        tk.Button(self.frame, text="Agregar Servicio", command=self.agregar_servicio).grid(row=2, column=0, columnspan=2)

        self.tree = tk.Listbox(self.frame)
        self.tree.grid(row=3, column=0, columnspan=2)
        self.tree.bind("<<ListboxSelect>>", self.seleccionar_servicio)

        self.cargar_servicios()

    def cargar_servicios(self):
        self.tree.delete(0, tk.END)
        servicios = self.controller.obtener_servicios()
        for servicio in servicios:
            self.tree.insert(tk.END, f"{servicio.id_servicio} - {servicio.descripcion} - {servicio.estatus}")

    def agregar_servicio(self):
        id_vehiculo = self.entry_id_vehiculo.get()
        descripcion = self.entry_descripcion.get()

        if not id_vehiculo or not descripcion:
            messagebox.showwarning("Validación", "Completa todos los campos.")
            return

        fecha_ingreso = datetime.now().strftime("%Y-%m-%d")
        self.controller.agregar_servicio(id_vehiculo, fecha_ingreso, descripcion, "En espera")
        self.cargar_servicios()

    def seleccionar_servicio(self, event):
        selection = self.tree.curselection()
        if selection:
            servicio_text = self.tree.get(selection[0])
            id_servicio = int(servicio_text.split(" - ")[0])

            nuevo_estatus = messagebox.askquestion("Actualizar Estado", "¿Cambiar estado del servicio?")

            if nuevo_estatus == "yes":
                estado_seleccionado = messagebox.askquestion("Seleccionar Estado", "¿Finalizado? (yes/no)")
                estado_final = "Finalizado" if estado_seleccionado == "yes" else "En proceso"
                self.controller.actualizar_servicio(id_servicio, estado_final)
                self.registrar_historial(id_servicio, estado_final)
                self.cargar_servicios()

    def registrar_historial(self, id_servicio, nuevo_estado):
        fecha_cambio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.controller.registrar_historial(id_servicio, nuevo_estado, fecha_cambio)
        messagebox.showinfo("Historial", "Historial del servicio actualizado correctamente.")

    def destroy(self):
        self.frame.destroy()
