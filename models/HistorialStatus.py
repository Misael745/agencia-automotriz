from datetime import datetime

class HistorialEstatus:
    def __init__(self, id_historial=None, id_servicio=None, fecha_cambio=None, estatus_anterior=None, estatus_nuevo=None, id_empleado=None):
        self.id_historial = id_historial
        self.id_servicio = id_servicio
        self.fecha_cambio = fecha_cambio or datetime.now()
        self.estatus_anterior = estatus_anterior
        self.estatus_nuevo = estatus_nuevo
        self.id_empleado = id_empleado

    def __str__(self):
        return f"🔄 Cambio: {self.estatus_anterior} → {self.estatus_nuevo}"