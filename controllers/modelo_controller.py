from DB.database import DB
from models.modelo import Modelo

class ModeloController:

    def agregar_modelo(self, id_marca, nombre_modelo):
        db = DB()
        try:
            cursor = db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "INSERT INTO modelos (id_marca, nombre_modelo) VALUES (%s, %s)"
            cursor.execute(sql, (id_marca, nombre_modelo))
            db.conn.commit()
            print("✅ Modelo agregado correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar modelo: {e}")
        finally:
            db.close()

    def obtener_modelos(self):
        db = DB()
        modelos = []
        try:
            cursor = db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return modelos

            sql = "SELECT id_modelo, id_marca, nombre_modelo FROM modelos"
            cursor.execute(sql)
            for fila in cursor.fetchall():
                modelo = Modelo(*fila)
                modelos.append(modelo)
        except Exception as e:
            print(f"❌ Error al obtener modelos: {e}")
        finally:
            db.close()
        return modelos

    def eliminar_modelo(self, id_modelo):
        db = DB()
        try:
            cursor = db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "DELETE FROM modelos WHERE id_modelo = %s"
            cursor.execute(sql, (id_modelo,))
            db.conn.commit()
            print("✅ Modelo eliminado correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar modelo: {e}")
        finally:
            db.close()

    def actualizar_modelo(self, id_modelo, nuevo_nombre):
        db = DB()
        try:
            cursor = db.get_cursor()
            if cursor is None:
                print("❌ No se pudo obtener el cursor.")
                return

            sql = "UPDATE modelos SET nombre_modelo = %s WHERE id_modelo = %s"
            cursor.execute(sql, (nuevo_nombre, id_modelo))
            db.conn.commit()
            print("✅ Modelo actualizado correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar modelo: {e}")
        finally:
            db.close()
