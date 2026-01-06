from model.usuarios_db import inicion_sesion
from view.main import pantalla_principal


def verificacion_inicio_sesion(usuario, clave, ventana):
    if inicion_sesion(usuario, clave) is None:
        return False
    else:
        ventana.destroy()
        pantalla_principal()
        return True