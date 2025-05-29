
from DB.database import DB
from models.servicio import Servicio

class ServicioController:
    def __init__(self):
        self.db = DB()

    def agregar_servicio(self, id_vehiculo, descripcion, refacciones, fecha_proximo_servicio):
        try:
            cursor = self.db.get_cursor()
            sql_servicio = "INSERT INTO servicios (id_vehiculo, descripcion, estatus, fecha_proximo_servicio) VALUES (%s, %s, 'En espera', %s)"
            cursor.execute(sql_servicio, (id_vehiculo, descripcion, fecha_proximo_servicio))
            servicio_id = cursor.lastrowid

            for ref_id, _, cantidad in refacciones:
                cursor.execute(
                    "INSERT INTO servicio_refaccion (id_servicio, id_refaccion, cantidad) VALUES (%s, %s, %s)",
                    (servicio_id, ref_id, cantidad)
                )

            self.db.conn.commit()
            self.generar_comprobante(servicio_id)

        except Exception as e:
            self.db.conn.rollback()
            print(f"❌ Error al agregar servicio: {e}")

    def generar_comprobante(self, servicio_id):
        try:
            cursor = self.db.get_cursor()

            cursor.execute("""
                SELECT s.fecha_ingreso, s.fecha_proximo_servicio, s.estatus, s.descripcion,
                       c.nombre, c.apellido, c.telefono, c.correo,
                       m.nombre_modelo, ma.nombre AS marca, v.placa
                FROM servicios s
                JOIN vehiculos v ON s.id_vehiculo = v.id_vehiculo
                JOIN clientes c ON v.id_cliente = c.id_cliente
                JOIN modelos m ON v.id_modelo = m.id_modelo
                JOIN marcas ma ON m.id_marca = ma.id_marca
                WHERE s.id_servicio = %s
            """, (servicio_id,))
            servicio = cursor.fetchone()

            cursor.execute("""
                SELECT r.nombre, sr.cantidad, r.precio_unitario
                FROM servicio_refaccion sr
                JOIN refacciones r ON sr.id_refaccion = r.id_refaccion
                WHERE sr.id_servicio = %s
            """, (servicio_id,))
            refacciones = cursor.fetchall()

            total = 0.00
            detalle = f"*** COMPROBANTE DE SERVICIO ***\n"
            detalle += f"ID Servicio: {servicio_id}\n"
            detalle += f"Fecha Ingreso: {servicio[0]}\n"
            detalle += f"Fecha Próximo Servicio: {servicio[1]}\n"
            detalle += f"Estatus: {servicio[2]}\n"
            detalle += f"Descripción: {servicio[3]}\n\n"

            detalle += f"Cliente: {servicio[4]} {servicio[5]}\n"
            detalle += f"Teléfono: {servicio[6]}\n"
            detalle += f"Correo: {servicio[7]}\n\n"

            detalle += f"Vehículo: {servicio[9]} {servicio[8]}\n"
            detalle += f"Placa: {servicio[10]}\n\n"

            detalle += f"Refacciones utilizadas:\n"
            detalle += f"{'-'*60}\n"
            for nombre, cantidad, precio in refacciones:
                subtotal = float(precio) * int(cantidad)
                total += subtotal
                detalle += f"{nombre} | Unidad: ${float(precio):.2f} x {cantidad} = ${subtotal:.2f}\n"

            detalle += f"{'-'*60}\n"
            detalle += f"TOTAL A PAGAR: ${total:.2f}\n"

            cursor.execute("""
                INSERT INTO comprobantes (id_servicio, monto_total, detalles)
                VALUES (%s, %s, %s)
            """, (servicio_id, total, detalle))

            self.db.conn.commit()
            print(f"✅ Comprobante generado para el servicio {servicio_id}")

        except Exception as e:
            self.db.conn.rollback()
            print(f"❌ Error al generar comprobante: {e}")

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

    def cambiar_estatus(self, id_servicio, nuevo_estatus):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("UPDATE servicios SET estatus=%s WHERE id_servicio=%s", (nuevo_estatus, id_servicio))
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            print(f"❌ Error al cambiar estatus: {e}")