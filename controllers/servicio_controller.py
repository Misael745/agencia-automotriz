from DB.database import DB
from models.servicio import Servicio

class ServicioController:
    def __init__(self):
        self.db = DB()

    def agregar_servicio(self, id_vehiculo, fecha_ingreso, descripcion, estatus="En espera"):
        try:
            cursor = self.db.get_cursor()
            sql = "INSERT INTO servicios (id_vehiculo, fecha_ingreso, descripcion, estatus) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_vehiculo, fecha_ingreso, descripcion, estatus))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al agregar servicio: {e}")

    def obtener_servicios(self):
        servicios = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM servicios")
            for row in cursor.fetchall():
                servicios.append(Servicio(*row))
        except Exception as e:
            print(f"❌ Error al obtener servicios: {e}")
        return servicios

    def actualizar_servicio(self, id_servicio, estatus):
        try:
            cursor = self.db.get_cursor()
            sql = "UPDATE servicios SET estatus = %s WHERE id_servicio = %s"
            cursor.execute(sql, (estatus, id_servicio))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al actualizar servicio: {e}")

    def eliminar_servicio(self, id_servicio):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("DELETE FROM servicios WHERE id_servicio = %s", (id_servicio,))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al eliminar servicio: {e}")