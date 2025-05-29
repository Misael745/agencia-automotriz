
from tkinter import *
from ui.servicio_ui import ServicioUI
from ui.comprobante_ui import ComprobanteUI
from ui.inicio_ui import InicioUI

class MenuTechUI:
    def __init__(self, root, empleado_actual):
        self.root = root
        self.empleado_actual = empleado_actual

        self.frame_container = Frame(self.root)
        self.frame_container.pack(fill="both", expand=True)

        menu_bar = Menu(self.root)

        # CRUD Menu
        crud_menu = Menu(menu_bar, tearoff=0)
        crud_menu.add_command(label="Servicios", command=self.mostrar_servicios)
        crud_menu.add_command(label="Comprobantes", command=self.mostrar_comprobantes)
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)

        # Opciones Menu (Inicio, Cerrar Sesión)
        opciones_menu = Menu(menu_bar, tearoff=0)
        opciones_menu.add_command(label="Inicio", command=self.mostrar_inicio)
        opciones_menu.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

        self.root.config(menu=menu_bar)

        self.vista_actual = None
        self.mostrar_inicio()

    def mostrar_inicio(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = InicioUI(self.frame_container, self.empleado_actual)

    def mostrar_servicios(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = ServicioUI(self.frame_container)

    def mostrar_comprobantes(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = ComprobanteUI(self.frame_container)

    def cerrar_sesion(self):
        self.root.destroy()
