class Marca:
    def __init__(self, id_marca=None, nombre=None):
        self.id_marca = id_marca
        self.nombre = nombre

    def __str__(self):
        return f"{self.nombre}"
