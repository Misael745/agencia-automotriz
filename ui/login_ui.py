import tkinter as tk
from tkinter import ttk, messagebox
from controllers.empleado_controller import EmpleadoController

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Agencia de Automóviles")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # Frame principal con ttk para estilo uniforme
        frame = ttk.Frame(root, padding=20)
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Inicio de Sesión", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.entry_usuario = ttk.Entry(frame, font=("Arial", 12))
        self.entry_usuario.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.entry_contraseña = ttk.Entry(frame, show="*", font=("Arial", 12))
        self.entry_contraseña.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        boton_login = ttk.Button(frame, text="Iniciar Sesión", command=self.validar_login)
        boton_login.grid(row=3, column=0, columnspan=2, pady=10)

    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Validación", "Por favor, ingresa usuario y contraseña.")
            return

        controller = EmpleadoController()
        try:
            emp = controller.validar_login(usuario, contraseña)
            if emp:
                self.mostrar_menu(emp)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar el login: {str(e)}")

    def mostrar_menu(self, emp):
        self.root.withdraw()
        root = tk.Toplevel()
        empleado_actual = f"{emp.nombre} {emp.apellido}"
        if emp.rol == 'administrador':
            from ui.menu_admin_ui import MenuAdminUI
            MenuAdminUI(root, empleado_actual)
        else:
            from ui.menu_tech_ui import MenuTechUI
            MenuTechUI(root, empleado_actual)
