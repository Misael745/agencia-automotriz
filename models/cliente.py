class Cliente:
    def __init__(self, id_cliente=None, nombre=None, apellido=None, telefono=None, correo=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"{self.nombre} {self.apellido} | 📞 {self.telefono}"