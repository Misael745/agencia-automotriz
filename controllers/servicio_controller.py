
from DB.database import DB
from models.servicio import Servicio

class ServicioController:
    def __init__(self):
        self.db = DB()

    def agregar_servicio(self, id_vehiculo, descripcion, refacciones):
        try:
            cursor = self.db.get_cursor()
            sql_servicio = "INSERT INTO servicios (id_vehiculo, descripcion, estatus) VALUES (%s, %s, 'En espera')"
            cursor.execute(sql_servicio, (id_vehiculo, descripcion))
            servicio_id = cursor.lastrowid

            for ref_id, _, cantidad in refacciones:
                cursor.execute(
                    "INSERT INTO servicio_refaccion (id_servicio, id_refaccion, cantidad) VALUES (%s, %s, %s)",
                    (servicio_id, ref_id, cantidad)
                )

            self.db.conn.commit()
            print("✅ Servicio y refacciones agregados correctamente.")
        except Exception as e:
            self.db.conn.rollback()
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

    def obtener_refacciones_servicio(self, id_servicio):
        refacciones = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""SELECT r.nombre, sr.cantidad, r.precio_unitario
                              FROM servicio_refaccion sr
                              JOIN refacciones r ON sr.id_refaccion = r.id_refaccion
                              WHERE sr.id_servicio = %s""", (id_servicio,))
            refacciones = cursor.fetchall()
        except Exception as e:
            print(f"❌ Error al obtener refacciones del servicio: {e}")
        return refacciones
