import bcrypt
from DB.database import DB
from models.empleado import Empleado

class EmpleadoController:
    def __init__(self):
        self.db = DB()

    def agregar_empleado(self, nombre, apellido, usuario, contraseña, rol):
        try:
            cursor = self.db.get_cursor()
            # 🔐 Cifrado de contraseña
            hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()
            sql = "INSERT INTO empleados (nombre, apellido, usuario, contraseña, rol) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, apellido, usuario, hashed, rol))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al agregar empleado: {e}")

    def obtener_empleados(self):
        empleados = []
        try:
            cursor = self.db.get_cursor()
            cursor.execute("SELECT * FROM empleados")
            for row in cursor.fetchall():
                empleado = Empleado(*row)
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
            # 🔐 Cifrado de contraseña al actualizar
            hashed = bcrypt.hashpw(contraseña.encode(), bcrypt.gensalt()).decode()
            sql = """
            UPDATE empleados SET nombre=%s, apellido=%s, usuario=%s, contraseña=%s, rol=%s 
            WHERE id_empleado=%s
            """
            cursor.execute(sql, (nombre, apellido, usuario, hashed, rol, id_empleado))
            self.db.conn.commit()
        except Exception as e:
            print(f"❌ Error al actualizar empleado: {e}")
