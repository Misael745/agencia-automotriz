class Empleado:
    def __init__(self, id_empleado=None, nombre=None, apellido=None, usuario=None, contraseña=None, rol=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.contraseña = contraseña  # En producción usar bcrypt
        self.rol = rol  # 'administrador' o 'tecnico'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"