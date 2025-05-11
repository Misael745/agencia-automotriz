import tkinter as tk
from ui.cliente_ui import ClienteUI
from ui.empleado_ui import EmpleadoUI
from ui.marca_ui import MarcaUI
from ui.modelo_ui import ModeloUI


class MenuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - Empleados")
        self.root.geometry("800x600")

        # Contenedor de las vistas
        self.frame_container = tk.Frame(self.root)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        # Menú principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Submenú para Empleados
        crud_menu = tk.Menu(self.menu_bar, tearoff=0)
        crud_menu.add_command(label="Empleados", command=self.mostrar_empleados)
        self.menu_bar.add_cascade(label="Gestión", menu=crud_menu)

        # Botón para cerrar sesión y cerrar conexión
        self.menu_bar.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        self.vista_actual = None
        self.mostrar_empleados()  # Carga la vista de empleados por defecto

    def limpiar_vista(self):
        if self.vista_actual:
            self.vista_actual.destroy()

    def mostrar_empleados(self):
        self.limpiar_vista()
        self.vista_actual = EmpleadoUI(self.frame_container)

    def cerrar_sesion(self):
        # Cierra la ventana principal
        self.root.destroy()

        # Cierra la conexión a la base de datos
        from DB.database import DB
        DB().close()

        # Reinicia el login
        import tkinter as tk
        from ui.login_ui import LoginUI

        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()
