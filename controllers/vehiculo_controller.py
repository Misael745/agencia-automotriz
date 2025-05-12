from DB.database import DB
from models.vehiculo import Vehiculo

class VehiculoController:
    def __init__(self):
        self.db = DB().get_cursor()

    def obtener_vehiculos(self):
        vehiculos = []
        try:
            self.db.execute("SELECT v.id_vehiculo, m.nombre_modelo, c.nombre, v.anio, v.placa FROM vehiculos v "
                            "JOIN modelos m ON v.id_modelo = m.id_modelo "
                            "JOIN clientes c ON v.id_cliente = c.id_cliente")
            for row in self.db.fetchall():
                vehiculos.append(Vehiculo(id_vehiculo=row[0], modelo=row[1], cliente=row[2], anio=row[3], placa=row[4]))
        except Exception as e:
            print(f"❌ Error al obtener vehículos: {e}")
        return vehiculos

    def agregar_vehiculo(self, id_modelo, id_cliente, anio, placa):
        try:
            sql = "INSERT INTO vehiculos (id_modelo, id_cliente, anio, placa) VALUES (%s, %s, %s, %s)"
            self.db.execute(sql, (id_modelo, id_cliente, anio, placa))
            self.db.connection.commit()
            print("✅ Vehículo agregado correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar vehículo: {e}")

    def actualizar_vehiculo(self, id_vehiculo, id_modelo, id_cliente, anio, placa):
        try:
            sql = "UPDATE vehiculos SET id_modelo=%s, id_cliente=%s, anio=%s, placa=%s WHERE id_vehiculo=%s"
            self.db.execute(sql, (id_modelo, id_cliente, anio, placa, id_vehiculo))
            self.db.connection.commit()
            print("✅ Vehículo actualizado correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar vehículo: {e}")

    def eliminar_vehiculo(self, id_vehiculo):
        try:
            sql = "DELETE FROM vehiculos WHERE id_vehiculo = %s"
            self.db.execute(sql, (id_vehiculo,))
            self.db.connection.commit()
            print("🗑️ Vehículo eliminado correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar vehículo: {e}")
