class Cliente:
    def __init__(self, nombre, apellido, telefono, localidad, direccion, factura_produccion, cuit):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.localidad = localidad
        self.direccion = direccion
        self.factura_produccion = factura_produccion
        self.cuit = cuit


class Producto:
    def __init__(self, nombre, categoria, unidad_medida, precio, cantidad):
        self.nombre = nombre
        self.categoria = categoria
        self.unidad_medida = unidad_medida
        self.precio = precio
        self.cantidad = cantidad


class Remito:
    def __init__(self):
        pass


class Operacion:
    def __init__(self):
        pass