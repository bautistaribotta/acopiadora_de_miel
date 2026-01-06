from model.usuarios_db import inicion_sesion


def verificacion_inicio_sesion(usuario, clave):
    if inicion_sesion(usuario, clave) is None:
        return False
    else:
        return True