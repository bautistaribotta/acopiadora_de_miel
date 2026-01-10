from model.login_db import inicion_sesion
from view.pantalla_principal_view import pantalla_administrador, pantalla_usuario


def verificacion_inicio_sesion(usuario, clave, ventana):
    resultado = inicion_sesion(usuario, clave)

    if resultado is None:
        return False
    else:
        ventana.destroy()
        if usuario == "administrador":
            pantalla_administrador()
        elif usuario == "usuario":
            pantalla_usuario()
        return True