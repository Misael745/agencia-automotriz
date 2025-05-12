class Refaccion:
    def __init__(self, id_refaccion=None, nombre=None, descripcion=None, precio_unitario=0.0, cantidad=0):
        self.id_refaccion = id_refaccion
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad

    def __str__(self):
        return f"⚙️ {self.nombre} | 💵 ${self.precio_unitario:.2f} | 📦 {self.cantidad} disponibles"
