import tkinter as tk
from tkinter import messagebox, ttk
from controllers.empleado_controller import EmpleadoController
from models.empleado_factory import EmpleadoFactory

class EmpleadoUI:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.controller = EmpleadoController()

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()
        self.rol_var = tk.StringVar()

        self.selected_id = None

        # Entrada de datos
        self.form_frame = tk.Frame(self.frame)
        self.form_frame.pack()

        tk.Label(self.form_frame, text="Nombre").grid(row=0, column=0)
        tk.Entry(self.form_frame, textvariable=self.nombre_var).grid(row=0, column=1)

        tk.Label(self.form_frame, text="Apellido").grid(row=1, column=0)
        tk.Entry(self.form_frame, textvariable=self.apellido_var).grid(row=1, column=1)

        tk.Label(self.form_frame, text="Usuario").grid(row=2, column=0)
        tk.Entry(self.form_frame, textvariable=self.usuario_var).grid(row=2, column=1)

        tk.Label(self.form_frame, text="Contraseña").grid(row=3, column=0)
        tk.Entry(self.form_frame, textvariable=self.contraseña_var, show="*").grid(row=3, column=1)

        tk.Label(self.form_frame, text="Rol").grid(row=4, column=0)
        self.rol_combo = ttk.Combobox(self.form_frame, textvariable=self.rol_var, state="readonly")
        self.rol_combo['values'] = ['administrador', 'tecnico']
        self.rol_combo.grid(row=4, column=1)

        # Botones
        tk.Button(self.form_frame, text="Agregar", command=self.agregar_empleado).grid(row=5, column=0)
        tk.Button(self.form_frame, text="Actualizar", command=self.actualizar_empleado).grid(row=5, column=1)
        tk.Button(self.form_frame, text="Eliminar", command=self.eliminar_empleado).grid(row=5, column=2)

        self.lista_empleados = tk.Listbox(self.frame, width=50)
        self.lista_empleados.pack()
        self.lista_empleados.bind("<<ListboxSelect>>", self.seleccionar_empleado)

        self.cargar_empleados()

    def cargar_empleados(self):
        self.lista_empleados.delete(0, tk.END)
        empleados = self.controller.obtener_empleados()
        for emp in empleados:
            self.lista_empleados.insert(tk.END, f"{emp.id_empleado} - {emp}")

    def seleccionar_empleado(self, event):
        try:
            index = self.lista_empleados.curselection()[0]
            texto = self.lista_empleados.get(index)
            id_empleado = int(texto.split(" - ")[0])
            empleado = next((e for e in self.controller.obtener_empleados() if e.id_empleado == id_empleado), None)
            if empleado:
                self.selected_id = empleado.id_empleado
                self.nombre_var.set(empleado.nombre)
                self.apellido_var.set(empleado.apellido)
                self.usuario_var.set(empleado.usuario)
                self.contraseña_var.set(empleado.contraseña)
                self.rol_var.set(empleado.rol)
        except IndexError:
            pass

    def agregar_empleado(self):
        empleado = EmpleadoFactory.crear_empleado(
            self.rol_var.get(),
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.usuario_var.get(),
            self.contraseña_var.get()
        )
        self.controller.agregar_empleado(
            empleado.nombre, empleado.apellido, empleado.usuario, empleado.contraseña, empleado.rol
        )
        self.limpiar_formulario()
        self.cargar_empleados()

    def actualizar_empleado(self):
        if self.selected_id is None:
            messagebox.showwarning("Selección", "Selecciona un empleado para actualizar.")
            return

        empleado = EmpleadoFactory.crear_empleado(
            self.rol_var.get(),
            self.nombre_var.get(),
            self.apellido_var.get(),
            self.usuario_var.get(),
            self.contraseña_var.get()
        )
        empleado.id_empleado = self.selected_id

        self.controller.actualizar_empleado(
            empleado.id_empleado,
            empleado.nombre,
            empleado.apellido,
            empleado.usuario,
            empleado.contraseña,
            empleado.rol
        )

        self.limpiar_formulario()
        self.cargar_empleados()

    def eliminar_empleado(self):
        if self.selected_id is None:
            messagebox.showwarning("Selección", "Selecciona un empleado para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este empleado?")
        if confirmar:
            self.controller.eliminar_empleado(self.selected_id)
            self.limpiar_formulario()
            self.cargar_empleados()

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.usuario_var.set("")
        self.contraseña_var.set("")
        self.rol_var.set("")
        self.selected_id = None

    def destroy(self):
        self.frame.destroy()
