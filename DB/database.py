import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None
    #se utiliza el principio singleton para la conexion a la base de  creando una instancia de la clase
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.connection = mysql.connector.connect(
                    host="localhost",
                    port=3306,  
                    user="root",
                    password="",
                    database="agencia_mantenimiento"
                )
                print("Conexión a BD exitosa!")
            except Error as e:
                print(f"Error al conectar a MySQL: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self._instance = None
            print("Conexión cerrada.")