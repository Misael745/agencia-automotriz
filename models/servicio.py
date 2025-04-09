from datetime import date

class Servicio:
    def __init__(self, id_servicio=None, id_vehiculo=None, fecha_ingreso=None, fecha_proximo_servicio=None, descripcion=None, estatus="En espera"):
        self.id_servicio = id_servicio
        self.id_vehiculo = id_vehiculo
        self.fecha_ingreso = fecha_ingreso or date.today()
        self.fecha_proximo_servicio = fecha_proximo_servicio
        self.descripcion = descripcion
        self.estatus = estatus  # 'En espera', 'En proceso', 'Finalizado'

    def __str__(self):
        return f"🔧 Servicio #{self.id_servicio} | Estado: {self.estatus}"

