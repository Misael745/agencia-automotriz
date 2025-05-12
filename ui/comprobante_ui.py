import tkinter as tk
from tkinter import messagebox, ttk
from controllers.comprobante_controller import ComprobanteController

class ComprobanteUI:
    def __init__(self, root):
        self.root = root
        self.controller = ComprobanteController()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Título
        tk.Label(self.frame, text="Gestión de Comprobantes", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

        # Tabla de Comprobantes
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Servicio", "Fecha", "Total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=1, column=0, columnspan=3)

        self.cargar_comprobantes()

        tk.Button(self.frame, text="Ver Comprobante", command=self.ver_comprobante).grid(row=2, column=0)
        tk.Button(self.frame, text="Generar PDF", command=self.generar_pdf).grid(row=2, column=1)

    def cargar_comprobantes(self):
        self.tree.delete(*self.tree.get_children())
        comprobantes = self.controller.obtener_comprobantes()
        for comp in comprobantes:
            self.tree.insert("", "end", values=(comp.id_comprobante, comp.id_servicio, comp.fecha_emision, comp.monto_total))

    def ver_comprobante(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debes seleccionar un comprobante.")
            return

        comp_id = self.tree.item(selected[0])['values'][0]
        detalles = self.controller.obtener_detalles_comprobante(comp_id)

        # Mostrar refacciones con cantidades
        messagebox.showinfo("Detalles del Comprobante", detalles)

    def generar_pdf(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debes seleccionar un comprobante.")
            return

        comp_id = self.tree.item(selected[0])['values'][0]
        self.controller.generar_comprobante_pdf(comp_id)
        messagebox.showinfo("Éxito", "Comprobante PDF generado correctamente.")

    def destroy(self):
        self.frame.destroy()