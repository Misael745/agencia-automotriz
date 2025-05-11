from models.empleado import Empleado

class Administrador(Empleado):
    def __init__(self, nombre, apellido, usuario, contraseña):
        super().__init__(nombre=nombre, apellido=apellido, usuario=usuario, contraseña=contraseña, rol='administrador')


class Tecnico(Empleado):
    def __init__(self, nombre, apellido, usuario, contraseña):
        super().__init__(nombre=nombre, apellido=apellido, usuario=usuario, contraseña=contraseña, rol='tecnico')


class EmpleadoFactory:
    @staticmethod
    def crear_empleado(rol, nombre, apellido, usuario, contraseña):
        if rol == 'administrador':
            return Administrador(nombre, apellido, usuario, contraseña)
        elif rol == 'tecnico':
            return Tecnico(nombre, apellido, usuario, contraseña)
        else:
            raise ValueError("Rol no válido. Debe ser 'administrador' o 'tecnico'.")
