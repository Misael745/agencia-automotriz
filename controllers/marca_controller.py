from DB.database import DB
from models.marca import Marca  # ← Asegúrate que aquí no esté Modelo

class MarcaController:
    def __init__(self):
        self.db = DB().get_cursor()

    def agregar_marca(self, nombre):
        try:
            sql = "INSERT INTO marcas (nombre) VALUES (%s)"
            self.db.execute(sql, (nombre,))
            self.db.connection.commit()
            print("✅ Marca agregada correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar marca: {e}")

    def obtener_marcas(self):
        marcas = []
        try:
            self.db.execute("SELECT * FROM marcas")
            for row in self.db.fetchall():
                marcas.append(Marca(id_marca=row[0], nombre=row[1]))  # 👈 Asegúrate que sea Marca y que los índices coincidan
        except Exception as e:
            print(f"❌ Error al obtener marcas: {e}")
        return marcas

    def eliminar_marca(self, id_marca):
        try:
            sql = "DELETE FROM marcas WHERE id_marca = %s"
            self.db.execute(sql, (id_marca,))
            self.db.connection.commit()
            print("🗑️ Marca eliminada correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar marca: {e}")

    def actualizar_marca(self, id_marca, nuevo_nombre):
        try:
            sql = "UPDATE marcas SET nombre = %s WHERE id_marca = %s"
            self.db.execute(sql, (nuevo_nombre, id_marca))
            self.db.connection.commit()
            print("✏️ Marca actualizada correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar marca: {e}")
