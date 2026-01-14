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
    def __init__(self, id_cliente, monto_total, total_en_dolares, total_en_kilos_miel, valor_dolar, valor_kilo_miel, fecha=None):
        self.id_cliente = id_cliente
        self.monto_total = monto_total
        self.total_en_dolares = total_en_dolares
        self.total_en_kilos_miel = total_en_kilos_miel
        self.valor_dolar = valor_dolar
        self.valor_kilo_miel = valor_kilo_miel
        self.fecha = fecha


class DetalleOperacion:
    def __init__(self, id_operacion, id_producto, cantidad):
        self.id_operacion = id_operacion
        self.id_producto = id_producto
        self.cantidad = cantidad