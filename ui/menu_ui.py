import tkinter as tk
from ui.cliente_ui import ClienteUI
from ui.empleado_ui import EmpleadoUI
from ui.marca_ui import MarcaUI
from ui.modelo_ui import ModeloUI

class MenuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")

        # Contenedor de las vistas
        self.frame_container = tk.Frame(self.root)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        # Menú principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Submenú para los CRUDs
        crud_menu = tk.Menu(self.menu_bar, tearoff=0)
        crud_menu.add_command(label="Clientes", command=self.mostrar_clientes)
        crud_menu.add_command(label="Empleados", command=self.mostrar_empleados)
        crud_menu.add_command(label="Marcas", command=self.mostrar_marcas)
        crud_menu.add_command(label="Modelos", command=self.mostrar_modelos)
        self.menu_bar.add_cascade(label="CRUDs", menu=crud_menu)

        # Opción de cerrar sesión
        self.menu_bar.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        self.vista_actual = None
        self.mostrar_clientes()  # Carga la vista por defecto

    def limpiar_vista(self):
        if self.vista_actual:
            self.vista_actual.destroy()

    def mostrar_clientes(self):
        self.limpiar_vista()
        self.vista_actual = ClienteUI(self.frame_container)

    def mostrar_empleados(self):
        self.limpiar_vista()
        self.vista_actual = EmpleadoUI(self.frame_container)

    def mostrar_marcas(self):
        self.limpiar_vista()
        self.vista_actual = MarcaUI(self.frame_container)

    def mostrar_modelos(self):
        self.limpiar_vista()
        self.vista_actual = ModeloUI(self.frame_container)

    def cerrar_sesion(self):
        self.root.destroy()  # Cierra la ventana principal

        # Reinicia el login
        import tkinter as tk
        from ui.login_ui import LoginUI
        from ui.main import iniciar_sistema  # Si necesitas reconectar algo más

        login_root = tk.Tk()
        LoginUI(login_root, on_login_success=iniciar_sistema)
        login_root.mainloop()

