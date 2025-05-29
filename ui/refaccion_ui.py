import tkinter as tk
from tkinter import ttk, messagebox
from controllers.refaccion_controller import RefaccionController

class RefaccionUI:
    def __init__(self, root):
        self.root = root
        self.controller = RefaccionController()

        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(1, weight=1)

        # Título
        ttk.Label(self.frame, text="Gestión de Refacciones", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Entradas
        self._crear_entrada("Nombre:", 1)
        self._crear_entrada("Descripción:", 2)
        self._crear_entrada("Precio Unitario:", 3)
        self._crear_entrada("Cantidad Disponible:", 4)

        # Botones
        botones_frame = ttk.Frame(self.frame)
        botones_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(botones_frame, text="Agregar", command=self.agregar_refaccion).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Actualizar", command=self.actualizar_refaccion).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Eliminar", command=self.eliminar_refaccion).pack(side="left", padx=5)

        # Tabla
        lista_frame = ttk.LabelFrame(self.frame, text="Refacciones Registradas", padding=10)
        lista_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        self.frame.rowconfigure(6, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(lista_frame, columns=("ID", "Nombre", "Descripción", "Precio", "Cantidad"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_refaccion)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.cargar_refacciones()

    def _crear_entrada(self, texto, fila):
        ttk.Label(self.frame, text=texto).grid(row=fila, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(self.frame, width=30)
        entry.grid(row=fila, column=1, padx=5, pady=5, sticky="ew")
        setattr(self, f"entry_{texto.lower().replace(' ', '_').replace(':', '').replace('.', '')}", entry)

    def cargar_refacciones(self):
        self.tree.delete(*self.tree.get_children())
        try:
            refacciones = self.controller.obtener_refacciones()
            for ref in refacciones:
                self.tree.insert("", "end", values=(ref.id_refaccion, ref.nombre, ref.descripcion, ref.precio_unitario, ref.cantidad))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las refacciones: {str(e)}")

    def agregar_refaccion(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        precio = self.entry_precio_unitario.get().strip()
        cantidad = self.entry_cantidad_disponible.get().strip()

        if not nombre or not descripcion or not precio or not cantidad:
            messagebox.showwarning("Validación", "Completa todos los campos.")
            return

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "El precio y la cantidad deben ser números.")
            return

        try:
            self.controller.agregar_refaccion(nombre, descripcion, precio, cantidad)
            self.cargar_refacciones()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Refacción agregada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la refacción: {str(e)}")

    def actualizar_refaccion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar una refacción")
            return

        ref_id = self.tree.item(selected[0])['values'][0]
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        precio = self.entry_precio_unitario.get().strip()
        cantidad = self.entry_cantidad_disponible.get().strip()

        if not nombre or not descripcion or not precio or not cantidad:
            messagebox.showwarning("Validación", "Completa todos los campos.")
            return

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "El precio y la cantidad deben ser números.")
            return

        try:
            self.controller.actualizar_refaccion(ref_id, nombre, descripcion, precio, cantidad)
            self.cargar_refacciones()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Refacción actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la refacción: {str(e)}")

    def eliminar_refaccion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Debes seleccionar una refacción")
            return

        ref_id = self.tree.item(selected[0])['values'][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta refacción?")
        if confirmar:
            try:
                self.controller.eliminar_refaccion(ref_id)
                self.cargar_refacciones()
                self.limpiar_formulario()
                messagebox.showinfo("Éxito", "Refacción eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la refacción: {str(e)}")

    def seleccionar_refaccion(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, values[2])
            self.entry_precio_unitario.delete(0, tk.END)
            self.entry_precio_unitario.insert(0, values[3])
            self.entry_cantidad_disponible.delete(0, tk.END)
            self.entry_cantidad_disponible.insert(0, values[4])

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio_unitario.delete(0, tk.END)
        self.entry_cantidad_disponible.delete(0, tk.END)

    def destroy(self):
        self.frame.destroy()
