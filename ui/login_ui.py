import tkinter as tk
from tkinter import messagebox
from controllers.empleado_controller import EmpleadoController
from ui.menu_admin_ui import MenuAdminUI
from ui.menu_tech_ui import MenuTechUI

class LoginUI:
    def __init__(self, root,on_login_success=None):

        self.root = root
        self.root.title("Login de Acceso")
        self.root.geometry("400x200")
        self.controller = EmpleadoController()

        self.usuario_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()
        self.intentos_fallidos = 0

        frame = tk.Frame(root)
        frame.pack(pady=50)

        tk.Label(frame, text="Usuario").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.usuario_var).grid(row=0, column=1)

        tk.Label(frame, text="Contraseña").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.contraseña_var, show="*").grid(row=1, column=1)

        tk.Button(frame, text="Ingresar", command=self.validar_login).grid(row=2, column=0, columnspan=2, pady=10)

    def validar_login(self):
        if self.intentos_fallidos >= 5:
            messagebox.showerror("Acceso bloqueado", "Demasiados intentos fallidos.")
            self.root.destroy()
            return

        usuario = self.usuario_var.get()
        contraseña = self.contraseña_var.get()

        for emp in self.controller.obtener_empleados():
            if emp.usuario == usuario:
                if self.controller.validar_contraseña(usuario, contraseña):
                    self.mostrar_menu(emp)
                    return

        self.intentos_fallidos += 1
        messagebox.showerror("Error", f"Credenciales inválidas. Intentos restantes: {5 - self.intentos_fallidos}")

    def mostrar_menu(self, empleado):
        self.root.destroy()
        if empleado.rol == 'administrador':
            root = tk.Tk()
            MenuAdminUI(root)
            root.mainloop()
        elif empleado.rol == 'tecnico':
            root = tk.Tk()
            MenuTechUI(root)
            root.mainloop()
