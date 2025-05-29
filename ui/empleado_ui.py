import tkinter as tk
from tkinter import messagebox, ttk
from controllers.empleado_controller import EmpleadoController
from models.empleado_factory import EmpleadoFactory

class EmpleadoUI:
    def __init__(self, root):
        self.root = root
        self.controller = EmpleadoController()
        self.selected_id = None

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()
        self.rol_var = tk.StringVar()

        # Frame principal con relleno
        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.crear_widgets()
        self.cargar_empleados()

    def crear_widgets(self):
        # Título principal
        ttk.Label(self.frame, text="Gestión de Empleados", font=("Arial", 16)).grid(row=0, column=0, pady=10, sticky="n")

        # Formulario
        form_frame = ttk.LabelFrame(self.frame, text="Datos del Empleado", padding=10)
        form_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        form_frame.columnconfigure(1, weight=1)

        campos = [
            ("Nombre", self.nombre_var),
            ("Apellido", self.apellido_var),
            ("Usuario", self.usuario_var),
            ("Contraseña", self.contraseña_var),
            ("Rol", self.rol_var)
        ]
        for i, (label, var) in enumerate(campos):
            ttk.Label(form_frame, text=label+":").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if label == "Rol":
                rol_combo = ttk.Combobox(form_frame, textvariable=var, values=["administrador", "tecnico"], state="readonly")
                rol_combo.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            elif label == "Contraseña":
                ttk.Entry(form_frame, textvariable=var, show="*").grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            else:
                ttk.Entry(form_frame, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=5)

        # Botones
        botones_frame = ttk.Frame(self.frame)
        botones_frame.grid(row=2, column=0, pady=5)
        botones = [
            ("Agregar", self.agregar_empleado),
            ("Actualizar", self.actualizar_empleado),
            ("Eliminar", self.eliminar_empleado),
            ("Limpiar", self.limpiar_formulario)
        ]
        for i, (text, cmd) in enumerate(botones):
            ttk.Button(botones_frame, text=text, command=cmd).grid(row=0, column=i, padx=5)

        # Lista de empleados
        lista_frame = ttk.LabelFrame(self.frame, text="Empleados Registrados", padding=10)
        lista_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.lista_empleados = tk.Listbox(lista_frame, height=10)
        self.lista_empleados.pack(side="left", fill="both", expand=True)
        self.lista_empleados.bind("<<ListboxSelect>>", self.seleccionar_empleado)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.lista_empleados.yview)
        self.lista_empleados.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def cargar_empleados(self):
        self.lista_empleados.delete(0, tk.END)
        try:
            empleados = self.controller.obtener_empleados()
            for emp in empleados:
                self.lista_empleados.insert(tk.END, f"{emp.id_empleado} - {emp}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

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
        if not self.validar_campos():
            return
        try:
            empleado = EmpleadoFactory.crear_empleado(
                self.rol_var.get(), self.nombre_var.get(), self.apellido_var.get(),
                self.usuario_var.get(), self.contraseña_var.get()
            )
            self.controller.agregar_empleado(empleado.nombre, empleado.apellido, empleado.usuario, empleado.contraseña, empleado.rol)
            self.limpiar_formulario()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado: {str(e)}")

    def actualizar_empleado(self):
        if self.selected_id is None:
            messagebox.showwarning("Selección", "Selecciona un empleado para actualizar.")
            return
        if not self.validar_campos():
            return
        try:
            empleado = EmpleadoFactory.crear_empleado(
                self.rol_var.get(), self.nombre_var.get(), self.apellido_var.get(),
                self.usuario_var.get(), self.contraseña_var.get()
            )
            empleado.id_empleado = self.selected_id
            self.controller.actualizar_empleado(
                empleado.id_empleado, empleado.nombre, empleado.apellido,
                empleado.usuario, empleado.contraseña, empleado.rol
            )
            self.limpiar_formulario()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado: {str(e)}")

    def eliminar_empleado(self):
        if self.selected_id is None:
            messagebox.showwarning("Selección", "Selecciona un empleado para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este empleado?")
        if confirm:
            try:
                self.controller.eliminar_empleado(self.selected_id)
                self.limpiar_formulario()
                self.cargar_empleados()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el empleado: {str(e)}")

    def limpiar_formulario(self):
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.usuario_var.set("")
        self.contraseña_var.set("")
        self.rol_var.set("")
        self.selected_id = None
        self.lista_empleados.selection_clear(0, tk.END)

    def validar_campos(self):
        if not self.nombre_var.get().strip():
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return False
        if not self.usuario_var.get().strip():
            messagebox.showwarning("Validación", "El usuario es obligatorio.")
            return False
        if not self.contraseña_var.get().strip():
            messagebox.showwarning("Validación", "La contraseña es obligatoria.")
            return False
        if not self.rol_var.get().strip():
            messagebox.showwarning("Validación", "El rol es obligatorio.")
            return False
        return True

    def destroy(self):
        self.frame.destroy()
