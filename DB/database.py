import pymysql
import logging
import os

logging.basicConfig(level=logging.INFO)

class DB:
    _instance = None  # Atributo estático para la instancia única

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # Ya inicializado, no volver a hacerlo

        self.conn = None
        self.cursor = None
        try:
            self.conn = pymysql.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", 3306)),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "1234"),
                db=os.getenv("MYSQL_DATABASE", "agencia_mantenimiento"),
                charset='utf8'
            )
            self.cursor = self.conn.cursor()
            logging.info("✅ Conexión a la base de datos establecida correctamente.")
        except Exception as e:
            logging.error(f"❌ Error al conectar a la base de datos: {e}")
            self.conn = None
            self.cursor = None

        self._initialized = True

    def get_cursor(self):
        if self.conn:
            logging.info("🔄 Cursor obtenido correctamente.")
            return self.conn.cursor()
        else:
            logging.error("⚠️ Intento de obtener cursor sin conexión activa.")
            return None

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            DB._instance = None  # Permite crear una nueva si se necesita en el futuro
            logging.info("🔒 Conexión cerrada correctamente.")
        except Exception as e:
            logging.error(f"❌ Error al cerrar la conexión: {e}")
