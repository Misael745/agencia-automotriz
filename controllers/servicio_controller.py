from DB.database import DB
from models.servicio import Servicio

class ServicioController:
    def __init__(self):
        self.db = DB()

    def obtener_servicios(self):
        servicios = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""
                SELECT s.id_servicio, s.id_vehiculo, v.placa, c.nombre, s.descripcion, s.estatus, s.fecha_ingreso, s.fecha_proximo_servicio
                FROM servicios s
                JOIN vehiculos v ON s.id_vehiculo = v.id_vehiculo
                JOIN clientes c ON v.id_cliente = c.id_cliente
            """)
            for row in cursor.fetchall():
                servicios.append(Servicio(*row))
        except Exception as e:
            print(f"❌ Error al obtener servicios: {e}")
        return servicios


    def obtener_refacciones_por_servicio(self, id_servicio):
            try:
                cursor = self.db.get_cursor()
                cursor.execute("""
                    SELECT r.id_refaccion, r.nombre, r.descripcion, r.cantidad AS stock, r.precio_unitario, sr.cantidad AS cantidad_usada
                    FROM servicio_refaccion sr
                    JOIN refacciones r ON sr.id_refaccion = r.id_refaccion
                    WHERE sr.id_servicio = %s
                """, (id_servicio,))
                return cursor.fetchall()
            except Exception as e:
                print(f"❌ Error al obtener refacciones por servicio: {e}")
                return []

    def actualizar_servicio(self, id_servicio, descripcion, fecha_proximo, estatus):
            try:
                cursor = self.db.get_cursor()
                cursor.execute("""
                    UPDATE servicios SET descripcion=%s, fecha_proximo_servicio=%s, estatus=%s
                    WHERE id_servicio=%s
                """, (descripcion, fecha_proximo, estatus, id_servicio))
                self.db.conn.commit()
                print("✅ Servicio actualizado correctamente.")
            except Exception as e:
                self.db.conn.rollback()
                print(f"❌ Error al actualizar servicio: {e}")

    def agregar_servicio(self, id_vehiculo, descripcion, refacciones, fecha_proximo_servicio):
            try:
                cursor = self.db.get_cursor()
                # Validar stock disponible
                for ref_id, _, cantidad_solicitada in refacciones:
                    cursor.execute("SELECT cantidad FROM refacciones WHERE id_refaccion = %s", (ref_id,))
                    row = cursor.fetchone()
                    if not row or row[0] < cantidad_solicitada:
                        raise Exception(f"Stock insuficiente para refacción ID {ref_id}. Solo hay {row[0] if row else 0} disponibles.")

                # Insertar servicio
                cursor.execute("""
                    INSERT INTO servicios (id_vehiculo, descripcion, estatus, fecha_proximo_servicio)
                    VALUES (%s, %s, 'En espera', %s)
                """, (id_vehiculo, descripcion, fecha_proximo_servicio))
                servicio_id = cursor.lastrowid

                # Insertar refacciones y actualizar stock
                for ref_id, _, cantidad in refacciones:
                    cursor.execute("""
                        INSERT INTO servicio_refaccion (id_servicio, id_refaccion, cantidad)
                        VALUES (%s, %s, %s)
                    """, (servicio_id, ref_id, cantidad))
                    cursor.execute("""
                        UPDATE refacciones SET cantidad = cantidad - %s WHERE id_refaccion = %s
                    """, (cantidad, ref_id))

                self.db.conn.commit()
                print(f"✅ Servicio {servicio_id} agregado correctamente con refacciones.")
            except Exception as e:
                self.db.conn.rollback()
                print(f"❌ Error al agregar servicio: {e}")
                raise e

    def obtener_servicios_por_cliente(self, cliente_nombre):
        servicios = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""
                SELECT s.id_servicio, s.id_vehiculo, v.placa, c.nombre, s.descripcion, s.estatus, s.fecha_ingreso, s.fecha_proximo_servicio
                FROM servicios s
                JOIN vehiculos v ON s.id_vehiculo = v.id_vehiculo
                JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE c.nombre LIKE %s
            """, (f"%{cliente_nombre}%",))
            for row in cursor.fetchall():
                servicios.append(Servicio(*row))  # Conversión a objetos Servicio
        except Exception as e:
            print(f"❌ Error al obtener servicios por cliente: {e}")
        return servicios
