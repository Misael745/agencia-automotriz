import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.servicio_controller import ServicioController

class InicioUI:
    def __init__(self, root, empleado_actual):
        self.root = root
        self.empleado_actual = empleado_actual
        self.controller = ServicioController()

        # Frame principal con ttk para consistencia
        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.crear_widgets()
        self.mostrar_grafico()

    def crear_widgets(self):
        # Título
        ttk.Label(self.frame, text=f"Bienvenido, {self.empleado_actual}", font=("Arial", 16)).grid(row=0, column=0, pady=10, sticky="n")

        # Filtro de periodo
        filtro_frame = ttk.Frame(self.frame)
        filtro_frame.grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Label(filtro_frame, text="Mostrar:").pack(side="left", padx=5)
        self.filtro_var = tk.StringVar(value="Total")
        filtro_combo = ttk.Combobox(filtro_frame, textvariable=self.filtro_var, state="readonly",
                                    values=["Hoy", "Esta semana", "Total", "Este mes", "Este año"])
        filtro_combo.pack(side="left", padx=5)
        filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.mostrar_grafico())

        # Área del gráfico
        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        self.frame.rowconfigure(2, weight=1)

    def mostrar_grafico(self):
        # Limpiar gráfico anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Obtener y filtrar servicios
        servicios = self.controller.obtener_servicios()
        filtro = self.filtro_var.get()
        hoy = datetime.now().date()
        if filtro == "Hoy":
            servicios = [s for s in servicios if s.fecha_ingreso == hoy]
        elif filtro == "Esta semana":
            semana = hoy - timedelta(days=hoy.weekday())
            servicios = [s for s in servicios if s.fecha_ingreso >= semana]
        elif filtro == "Este mes":
            servicios = [s for s in servicios if s.fecha_ingreso.month == hoy.month and s.fecha_ingreso.year == hoy.year]
        elif filtro == "Este año":
            servicios = [s for s in servicios if s.fecha_ingreso.year == hoy.year]

        # Contar estados
        conteo = {"En espera": 0, "En proceso": 0, "Finalizado": 0}
        for s in servicios:
            conteo[s.estatus] += 1

        # Crear gráfico
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        estados = list(conteo.keys())
        cantidades = list(conteo.values())
        colores = ['#FFA500', '#1E90FF', '#32CD32']
        ax.bar(estados, cantidades, color=colores)
        ax.set_title("Estatus de Servicios")
        ax.set_ylabel("Cantidad")
        ax.set_xlabel("Estado")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Mostrar gráfico
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def destroy(self):
        self.frame.destroy()
