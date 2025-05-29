from DB.database import DB
from  models.empleado_factory import EmpleadoFactory
import hashlib

class EmpleadoController:
    def __init__(self):
        self.db = DB()

    def agregar_empleado(self, nombre, apellido, usuario, contraseña, rol):
        try:
            cursor = self.db.get_cursor()
            sql = "INSERT INTO empleados (nombre, apellido, usuario, contraseña, rol) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, apellido, usuario, contraseña, rol))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al agregar empleado: {e}")

    def obtener_empleados(self):
        empleados = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT id_empleado, nombre, apellido, usuario, contraseña, rol FROM empleados")
            for row in cursor.fetchall():
                id_empleado, nombre, apellido, usuario, contraseña, rol = row
                empleado = EmpleadoFactory.crear_empleado(rol, nombre, apellido, usuario, contraseña)
                empleado.id_empleado = id_empleado
                empleados.append(empleado)
        except Exception as e:
            print(f"❌ Error al obtener empleados: {e}")
        return empleados

    def eliminar_empleado(self, id_empleado):
        try:
            cursor = self.db.get_cursor()
            cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (id_empleado,))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al eliminar empleado: {e}")

    def actualizar_empleado(self, id_empleado, nombre, apellido, usuario, contraseña, rol):
        try:
            cursor = self.db.get_cursor()
            sql = """
            UPDATE empleados SET nombre=%s, apellido=%s, usuario=%s, contraseña=%s, rol=%s 
            WHERE id_empleado=%s
            """
            cursor.execute(sql, (nombre, apellido, usuario, contraseña, rol, id_empleado))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al actualizar empleado: {e}")

    def validar_contraseña(self, usuario, contraseña):
        try:
            cursor = self.db.get_cursor()
            sql = "SELECT * FROM empleados WHERE usuario = %s AND contraseña = SHA2(%s, 256)"
            cursor.execute(sql, (usuario, contraseña))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"❌ Error al validar contraseña: {e}")
            return False

    def validar_login(self, usuario, contraseña):
        try:
            cursor = self.db.get_cursor()
            hashed = hashlib.sha256(contraseña.encode()).hexdigest()
            cursor.execute(
                "SELECT id_empleado, nombre, apellido, usuario, contraseña, rol FROM empleados WHERE usuario=%s AND contraseña=%s",
                (usuario, hashed)
            )
            row = cursor.fetchone()
            if row:
                id_empleado, nombre, apellido, usuario, contraseña_db, rol = row
                empleado = EmpleadoFactory.crear_empleado(rol, nombre, apellido, usuario, contraseña_db)
                empleado.id_empleado = id_empleado
                return empleado
            else:
                return None
        except Exception as e:
            print(f"❌ Error al validar login: {e}")
            return None
