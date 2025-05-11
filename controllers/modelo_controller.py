from DB.database import DB
from models.modelo import Modelo

class ModeloController:
    def __init__(self):
        self.db = DB()

    def agregar_modelo(self, id_marca, nombre_modelo):
        try:
            cursor = self.db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "INSERT INTO modelos (id_marca, nombre_modelo) VALUES (%s, %s)"
            cursor.execute(sql, (id_marca, nombre_modelo))
            self.db.conn.commit()
            print("✅ Modelo agregado correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar modelo: {e}")

    def obtener_modelos(self):
        try:
            cursor = self.db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return []

            cursor.execute("SELECT id_modelo, id_marca, nombre_modelo FROM modelos")
            modelos = [Modelo(*row) for row in cursor.fetchall()]
            return modelos
        except Exception as e:
            print(f"❌ Error al obtener modelos: {e}")
            return []

    def actualizar_modelo(self, id_modelo, nombre_modelo, id_marca):
        try:
            cursor = self.db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "UPDATE modelos SET nombre_modelo = %s, id_marca = %s WHERE id_modelo = %s"
            cursor.execute(sql, (nombre_modelo, id_marca, id_modelo))
            self.db.conn.commit()
            print("✅ Modelo actualizado correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar modelo: {e}")

    def eliminar_modelo(self, id_modelo):
        try:
            cursor = self.db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "DELETE FROM modelos WHERE id_modelo = %s"
            cursor.execute(sql, (id_modelo,))
            self.db.conn.commit()
            print("🗑️ Modelo eliminado correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar modelo: {e}")
