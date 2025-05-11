import tkinter as tk
from ui.servicio_ui import ServicioUI
from DB.database import DB

class MenuTechUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Técnico")
        self.root.geometry("900x600")

        self.frame_container = tk.Frame(self.root)
        self.frame_container.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar.add_command(label="Gestión Servicios", command=self.mostrar_servicios)
        self.menu_bar.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        self.vista_actual = None
        self.mostrar_servicios()

    def limpiar_vista(self):
        if self.vista_actual:
            self.vista_actual.destroy()

    def mostrar_servicios(self):
        self.limpiar_vista()
        self.vista_actual = ServicioUI(self.frame_container)

    def cerrar_sesion(self):
        self.root.destroy()
        DB().close()

        import tkinter as tk
        from ui.login_ui import LoginUI

        login_root = tk.Tk()
        LoginUI(login_root)
        login_root.mainloop()
