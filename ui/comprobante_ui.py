import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.comprobante_controller import ComprobanteController

class ComprobanteUI:
    def __init__(self, root):
        self.root = root
        self.controller = ComprobanteController()

        self.frame = tk.Frame(self.root, bg="lightsteelblue")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Listado de Comprobantes", font=("Arial", 16), bg="lightsteelblue").pack(pady=10)

        # Filtros de búsqueda
        filtro_frame = tk.Frame(self.frame, bg="lightsteelblue")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="Buscar por ID, Cliente o Fecha:", bg="lightsteelblue").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filtro_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5)

        tk.Label(filtro_frame, text="Desde:", bg="lightsteelblue").grid(row=0, column=2, padx=5)
        self.fecha_desde = DateEntry(filtro_frame, width=12, date_pattern='yyyy-mm-dd')
        self.fecha_desde.grid(row=0, column=3, padx=5)

        tk.Label(filtro_frame, text="Hasta:", bg="lightsteelblue").grid(row=0, column=4, padx=5)
        self.fecha_hasta = DateEntry(filtro_frame, width=12, date_pattern='yyyy-mm-dd')
        self.fecha_hasta.grid(row=0, column=5, padx=5)

        tk.Button(filtro_frame, text="Aplicar Filtro", command=self.cargar_comprobantes, bg="green", fg="white").grid(row=0, column=6, padx=5)

        # Tabla de comprobantes
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Servicio", "Fecha", "Total"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Botones extra
        btn_frame = tk.Frame(self.frame, bg="lightsteelblue")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Ver Detalles", command=self.ver_detalles, bg="blue", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Generar PDF", command=self.generar_pdf, bg="purple", fg="white").pack(side="left", padx=5)

        self.cargar_comprobantes()

    def cargar_comprobantes(self):
        search_text = self.search_var.get().lower()
        fecha_d = self.fecha_desde.get_date()
        fecha_h = self.fecha_hasta.get_date()

        self.tree.delete(*self.tree.get_children())
        comprobantes = self.controller.obtener_comprobantes()
        for c in comprobantes:
            if (search_text in str(c.id_comprobante).lower() or
                search_text in c.detalles.lower() or
                search_text in c.fecha_emision.strftime("%Y-%m-%d")) and (fecha_d <= c.fecha_emision.date() <= fecha_h):
                self.tree.insert("", "end", values=(c.id_comprobante, c.id_servicio, c.fecha_emision.strftime("%Y-%m-%d"), f"${c.monto_total:.2f}"))

    def ver_detalles(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un comprobante.")
            return
        id_comprobante = self.tree.item(selected[0])["values"][0]
        detalles = self.controller.obtener_detalles_comprobante(id_comprobante)
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Detalles Comprobante #{id_comprobante}")
        text = tk.Text(ventana, wrap=tk.WORD, width=80, height=20)
        text.insert("1.0", detalles)
        text.config(state="disabled")
        text.pack(padx=10, pady=10)

    def generar_pdf(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un comprobante.")
            return
        id_comprobante = self.tree.item(selected[0])["values"][0]
        self.controller.generar_comprobante_pdf(id_comprobante)
        messagebox.showinfo("Éxito", f"Comprobante #{id_comprobante} exportado como PDF.")

    def destroy(self):
        self.frame.destroy()
