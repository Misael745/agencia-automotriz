from DB.database import DB
from models.refaccion import Refaccion

class RefaccionController:
    def __init__(self):
        self.db = DB()

    def obtener_refacciones(self):
        refacciones = []
        try:
            cursor = self.db.get_cursor()
            if cursor is None:
                print("❌ Error: no se pudo obtener cursor (la base de datos no está conectada).")
                return []
            cursor.execute("SELECT id_refaccion, nombre, descripcion, precio_unitario, cantidad FROM refacciones")
            for row in cursor.fetchall():
                refacciones.append(Refaccion(*row))
        except Exception as e:
            print(f"❌ Error al obtener refacciones: {e}")
        return refacciones

    def obtener_cantidad_disponible(self, ref_id):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT cantidad FROM refacciones WHERE id_refaccion = %s", (ref_id,))
            row = cursor.fetchone()
            return row[0] if row else 0
        except Exception as e:
            print(f"❌ Error al obtener cantidad disponible: {e}")
            return 0

    def agregar_refaccion(self, nombre, descripcion, precio_unitario, cantidad):
        try:
            cursor = self.db.get_cursor()
            sql = "INSERT INTO refacciones (nombre, descripcion, precio_unitario, cantidad) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio_unitario, cantidad))
            self.db.conn.commit()
            print("✅ Refacción agregada correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar refacción: {e}")

    def actualizar_refaccion(self, id_refaccion, nombre, descripcion, precio_unitario, cantidad):
        try:
            cursor = self.db.get_cursor()
            sql = "UPDATE refacciones SET nombre=%s, descripcion=%s, precio_unitario=%s, cantidad=%s WHERE id_refaccion=%s"
            cursor.execute(sql, (nombre, descripcion, precio_unitario, cantidad, id_refaccion))
            self.db.conn.commit()
            print("✅ Refacción actualizada correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar refacción: {e}")

    def eliminar_refaccion(self, id_refaccion):
        try:
            cursor = self.db.get_cursor()
            sql = "DELETE FROM refacciones WHERE id_refaccion = %s"
            cursor.execute(sql, (id_refaccion,))
            self.db.conn.commit()
            print("🗑️ Refacción eliminada correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar refacción: {e}")

    def obtener_refaccion_por_id(self, ref_id):
            try:
                cursor = self.db.get_cursor()
                cursor.execute("SELECT id_refaccion, nombre, descripcion, cantidad, precio_unitario FROM refacciones WHERE id_refaccion=%s", (ref_id,))
                row = cursor.fetchone()
                if row:
                    return Refaccion(*row)
                else:
                    return None
            except Exception as e:
                print(f"❌ Error al obtener refacción por ID: {e}")
                return None