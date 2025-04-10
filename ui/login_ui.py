import tkinter as tk
from tkinter import messagebox
from controllers.empleado_controller import EmpleadoController
import bcrypt

class LoginUI:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login de Administrador")
        self.controller = EmpleadoController()
        self.on_login_success = on_login_success

        self.usuario_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()

        frame = tk.Frame(root)
        frame.pack(pady=50)

        tk.Label(frame, text="Usuario").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.usuario_var).grid(row=0, column=1)

        tk.Label(frame, text="Contraseña").grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.contraseña_var, show="*").grid(row=1, column=1)

        tk.Button(frame, text="Ingresar", command=self.validar_login).grid(row=2, column=0, columnspan=2, pady=10)

    def validar_login(self):
        usuario = self.usuario_var.get()
        contraseña = self.contraseña_var.get()

        for emp in self.controller.obtener_empleados():
            if emp.usuario == usuario and emp.rol == "administrador":
                if bcrypt.checkpw(contraseña.encode(), emp.contraseña.encode()):
                    self.on_login_success()
                    return
        messagebox.showerror("Error", "Credenciales inválidas")
