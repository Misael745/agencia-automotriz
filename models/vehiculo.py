class Vehiculo:
    def __init__(self, id_vehiculo=None, modelo=None, cliente=None, anio=None, placa=None):
        self.id_vehiculo = id_vehiculo
        self.modelo = modelo
        self.cliente = cliente
        self.anio = anio
        self.placa = placa

    def __str__(self):
        return f"🚗 {self.modelo} - {self.placa} | Cliente: {self.cliente} | Año: {self.anio}"
