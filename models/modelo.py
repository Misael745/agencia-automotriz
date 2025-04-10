class Modelo:
    def __init__(self, id_modelo, id_marca, nombre_modelo):
        self.id_modelo = id_modelo
        self.id_marca = id_marca
        self.nombre_modelo = nombre_modelo

    def __str__(self):
        return f"{self.nombre_modelo} (Marca ID: {self.id_marca})"