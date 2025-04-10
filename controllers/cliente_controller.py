from DB.database import DB
from models.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.db = DB()
        self.conn = self.db.conn

    def agregar_cliente(self, nombre, apellido, telefono, correo):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO clientes (nombre, apellido, telefono, correo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, apellido, telefono, correo))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar cliente: {e}")
            return False

    def obtener_clientes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return []

    def eliminar_cliente(self, id_cliente):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            self.conn.commit()
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, correo):
        try:
            cursor = self.conn.cursor()
            sql = """
                UPDATE clientes SET nombre=%s, apellido=%s, telefono=%s, correo=%s
                WHERE id_cliente=%s
            """
            cursor.execute(sql, (nombre, apellido, telefono, correo, id_cliente))
            self.conn.commit()
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
