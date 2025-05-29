from tkinter import ttk, Menu
import tkinter as tk
from ui.cliente_ui import ClienteUI
from ui.empleado_ui import EmpleadoUI
from ui.marca_ui import MarcaUI
from ui.modelo_ui import ModeloUI
from ui.vehiculo_ui import VehiculoUI
from ui.refaccion_ui import RefaccionUI
from ui.servicio_ui import ServicioUI
from ui.comprobante_ui import ComprobanteUI
from ui.inicio_ui import InicioUI

class MenuAdminUI:
    def __init__(self, root, empleado_actual):
        self.root = root
        self.empleado_actual = empleado_actual

        self.frame_container = ttk.Frame(self.root, padding=10)
        self.frame_container.pack(fill="both", expand=True)
        self.frame_container.columnconfigure(0, weight=1)
        self.frame_container.rowconfigure(0, weight=1)

        menu_bar = Menu(self.root)

        crud_menu = Menu(menu_bar, tearoff=0)
        secciones_crud = [
            ("Clientes", ClienteUI),
            ("Empleados", EmpleadoUI),
            ("Marcas", MarcaUI),
            ("Modelos", ModeloUI),
            ("Vehículos", VehiculoUI),
            ("Refacciones", RefaccionUI),
            ("Servicios", ServicioUI),
            ("Comprobantes", ComprobanteUI)
        ]
        for nombre, clase_vista in secciones_crud:
            crud_menu.add_command(label=nombre, command=lambda c=clase_vista: self.mostrar_vista(c))
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)

        opciones_menu = Menu(menu_bar, tearoff=0)
        opciones_menu.add_command(label="Inicio", command=self.mostrar_inicio)
        opciones_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

        self.root.config(menu=menu_bar)

        self.vista_actual = None
        self.mostrar_inicio()

    def mostrar_vista(self, vista_clase, *args):
        if self.vista_actual:
            self.vista_actual.destroy()
        try:
            self.vista_actual = vista_clase(self.frame_container, *args)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Ocurrió un error al cargar {vista_clase.__name__}:\n{e}")
            print(f"Error en {vista_clase.__name__}: {e}")

    def mostrar_inicio(self):
        self.mostrar_vista(InicioUI, self.empleado_actual)

    def cerrar_sesion(self):
        self.root.destroy()  # Cerrar la ventana actual
        from ui.login_ui import LoginUI
        nueva_raiz = tk.Tk()
        LoginUI(nueva_raiz)
        nueva_raiz.mainloop()
