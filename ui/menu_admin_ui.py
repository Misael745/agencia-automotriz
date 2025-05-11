import tkinter as tk
from ui.empleado_ui import EmpleadoUI
from ui.servicio_ui import ServicioUI
from ui.cliente_ui import ClienteUI
from ui.marca_ui import MarcaUI
from ui.modelo_ui import ModeloUI
from DB.database import DB

class MenuAdminUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Administrador")
        self.root.geometry("900x600")

        self.frame_container = tk.Frame(self.root)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        crud_menu = tk.Menu(self.menu_bar, tearoff=0)
        crud_menu.add_command(label="Gestión Empleados", command=self.mostrar_empleados)
        crud_menu.add_command(label="Gestión Servicios", command=self.mostrar_servicios)
        crud_menu.add_command(label="Gestión Clientes", command=self.mostrar_clientes)
        crud_menu.add_command(label="Gestión Marcas", command=self.mostrar_marcas)
        crud_menu.add_command(label="Gestión Modelos", command=self.mostrar_modelos)
        self.menu_bar.add_cascade(label="Administración", menu=crud_menu)

        self.menu_bar.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        self.vista_actual = None
        self.mostrar_empleados()

    def limpiar_vista(self):
        if self.vista_actual:
            self.vista_actual.destroy()

    def mostrar_empleados(self):
        self.limpiar_vista()
        self.vista_actual = EmpleadoUI(self.frame_container)

    def mostrar_servicios(self):
        self.limpiar_vista()
        self.vista_actual = ServicioUI(self.frame_container)

    def mostrar_clientes(self):
        self.limpiar_vista()
        self.vista_actual = ClienteUI(self.frame_container)

    def mostrar_marcas(self):
        self.limpiar_vista()
        self.vista_actual = MarcaUI(self.frame_container)

    def mostrar_modelos(self):
        self.limpiar_vista()
        self.vista_actual = ModeloUI(self.frame_container)
        self.vista_actual.pack(fill=tk.BOTH, expand=True)



    def cerrar_sesion(self):
        self.root.destroy()
        DB().close()

        import tkinter as tk
        from ui.login_ui import LoginUI

        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()