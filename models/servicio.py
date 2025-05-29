from DB.database import DB

class Servicio:
    def __init__(self, id_servicio, id_vehiculo, placa, cliente, descripcion, estatus, fecha_ingreso, fecha_proximo_servicio):
        self.id_servicio = id_servicio
        self.id_vehiculo = id_vehiculo
        self.placa = placa
        self.cliente = cliente
        self.descripcion = descripcion
        self.estatus = estatus
        self.fecha_ingreso = fecha_ingreso
        self.fecha_proximo_servicio = fecha_proximo_servicio

