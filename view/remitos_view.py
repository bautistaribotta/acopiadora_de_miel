import tkinter as tk
from tkinter import ttk
from view.estilos import *
from controller.clientes_controlador import listar_clientes_controlador

ventana_remitos_instancia = None


def remitos():
    global ventana_remitos_instancia
    if ventana_remitos_instancia is not None and ventana_remitos_instancia.winfo_exists():
        ventana_remitos_instancia.lift()
        return

    ventana_remitos = tk.Toplevel()
    ventana_remitos_instancia = ventana_remitos

    ventana_remitos.title("Nuevo Remito")
    ventana_remitos.configure(bg=color_primario)
    ventana_remitos.resizable(False, False)
    
    # Configuro las dimensiones
    centrar_ventana_interna(ventana_remitos, 400, 300) # Un poco mas alto para que entre la lista desplegable
    
    try:
        ventana_remitos.iconbitmap(obtener_ruta_recurso("colmena.ico"))
    except:
        pass
    
    # --- Obtengo datos ---
    try:
        clientes_db = listar_clientes_controlador()
    except Exception:
        clientes_db = []

    # Creo lista de strings para mostrar
    lista_clientes_display = []
    if clientes_db:
        for c in clientes_db:
            lista_clientes_display.append(f"{c[1]} (ID: {c[0]})")

    # --- Configuro laInterfaz ---
    label_titulo = tk.Label(ventana_remitos, text="Seleccione Cliente", bg=color_primario, fg="white", font=fuente_titulos)
    label_titulo.pack(pady=(30, 20))


    # Configuro el frame contenedor
    frame_buscador = tk.Frame(ventana_remitos, bg=color_primario)
    frame_buscador.pack(pady=10, padx=20)

    # Configuro el Entry (Campo de texto)
    entry_cliente = tk.Entry(frame_buscador, font=fuente_texto, width=30)
    entry_cliente.pack()
    
    # Configuro el Listbox (Lista desplegable simulada)
    # Importante: La hago hija del frame para posicionarse relativa al entry fácilmente,
    # y uso lift() al mostrarla.
    lista_sugerencias = tk.Listbox(frame_buscador, font=fuente_texto, height=5)
    
    def actualizar_lista(data):
        lista_sugerencias.delete(0, tk.END)
        for item in data:
            lista_sugerencias.insert(tk.END, item)
            
        if data:
            # Uso 'in_' para posicionar relativo al entry, rely=1.0 es justo abajo
            lista_sugerencias.place(in_=entry_cliente, x=0, rely=1.0, relwidth=1.0)
            lista_sugerencias.lift()
        else:
            lista_sugerencias.place_forget()

    def filtrar(event):
        # Gestiono la navegación
        if event.keysym == 'Down':
            if lista_sugerencias.winfo_viewable():
                lista_sugerencias.focus_set()
                if lista_sugerencias.size() > 0:
                    lista_sugerencias.selection_set(0)
            return
        if event.keysym in ('Up', 'Left', 'Right', 'Return'):
            return

        typed = entry_cliente.get().lower()
        if typed == '':
            lista_sugerencias.place_forget()
        else:
            # Realizo filtrado simple
            filtered = [x for x in lista_clientes_display if typed in x.lower()]
            actualizar_lista(filtered[:5]) # Limito a 5

    def seleccionar_de_lista(event):
        seleccion = lista_sugerencias.curselection()
        if seleccion:
            item = lista_sugerencias.get(seleccion[0])
            entry_cliente.delete(0, tk.END)
            entry_cliente.insert(0, item)
            lista_sugerencias.place_forget()
            entry_cliente.focus_set()

    entry_cliente.bind("<KeyRelease>", filtrar)
    lista_sugerencias.bind("<<ListboxSelect>>", seleccionar_de_lista)
    lista_sugerencias.bind("<Return>", lambda e: seleccionar_de_lista(e))
    
    # Cierro lista si se hace clic fuera
    def cerrar_lista(event):
        widget = event.widget
        # Si el clic no fue en el entry ni en la lista, cierro
        if widget != entry_cliente and widget != lista_sugerencias:
            lista_sugerencias.place_forget()
            
    ventana_remitos.bind("<Button-1>", cerrar_lista)


    # --- Botón Continuar ---
    def on_continuar():
        seleccion = entry_cliente.get()
        if not seleccion:
            return

        # Lógica siguiente...

    boton_seleccionar = ttk.Button(ventana_remitos, text="Continuar", style="BotonSecundario.TButton")
    boton_seleccionar.configure(command=on_continuar, cursor="hand2")
    # Aumento el padding para proteger el área donde se despliega la lista
    boton_seleccionar.pack(pady=(50, 20))


if __name__ == "__main__":
    remitos()