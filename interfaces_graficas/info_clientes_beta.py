import tkinter as tk
from tkinter import ttk
from utilidades.configuracion import *


def informacion_cliente():
    ventana_info_cliente = tk.Toplevel(root)
    ventana_info_cliente.title("Informacion del cliente")
    ventana_info_cliente.configure(bg=color_primario)
    
    # Dimensiones y centrado (Achicar ventana)
    ancho_ventana = 900
    alto_ventana = 600
    centrar_ventana(ventana_info_cliente, ancho_ventana, alto_ventana)

    # --- Frame Superior (Datos y Valores) ---
    # Al usar el fondo de la ventana como color_primario, este frame se integra visualmente
    frame_superior = tk.Frame(ventana_info_cliente, bg=color_primario)
    frame_superior.pack(side="top", fill="x", expand=False, padx=20, pady=5)

    # Sub-frame para datos del cliente (Izquierda)
    frame_datos = tk.Frame(frame_superior, bg=color_primario)
    frame_datos.pack(side="left", fill="both", expand=True)

    labels_datos = ["ID", "Telefono", "Nombre", "Apellido", "Localidad", "Calle", "Factura (Si/No)", "CUIT"]

    for i, label_text in enumerate(labels_datos):
        row = i // 2
        col_start = (i % 2) * 2
        
        # Etiqueta del campo
        lbl_titulo = tk.Label(frame_datos, text=label_text + ":", bg=color_primario, fg="white", font=("Arial", 10, "bold"))
        lbl_titulo.grid(row=row, column=col_start, sticky="w", pady=1, padx=(10, 5))
        
        # Valor (Label en lugar de Entry)
        lbl_valor = tk.Label(frame_datos, text="---", bg=color_primario, fg="white", font=("Arial", 10))
        lbl_valor.grid(row=row, column=col_start + 1, sticky="w", pady=1, padx=(0, 30))
    
    # Configurar columnas para que ocupen espacio
    frame_datos.grid_columnconfigure(1, weight=1)
    frame_datos.grid_columnconfigure(3, weight=1)
    
    # Sub-frame derecho (Valores y Botones)
    frame_derecho = tk.Frame(frame_superior, bg=color_primario)
    frame_derecho.pack(side="right", fill="y", padx=(20, 0))

    # Sub-frame para valores
    frame_valores = tk.Frame(frame_derecho, bg=color_primario)
    frame_valores.pack(side="top", pady=(0, 10))

    valores = ["Kilo de Miel", "Valor Dolar", "Pesos Argentinos"]

    for i, valor_text in enumerate(valores):
        frame_val_item = tk.Frame(frame_valores, bg=color_primario)
        frame_val_item.pack(side="left", padx=10)

        lbl = tk.Label(frame_val_item, text=valor_text, bg=color_primario, fg="white", font=("Arial", 10, "bold"))
        lbl.pack()
        
        lbl_val = tk.Label(frame_val_item, text="---", bg="white", fg="black", font=("Arial", 11, "bold"), width=10, relief="sunken")
        lbl_val.pack(pady=2)

    # Sub-frame para botones
    frame_botones = tk.Frame(frame_derecho, bg=color_primario)
    frame_botones.pack(side="top", fill="x", pady=5)

    botones = ["Nueva", "Editar", "Eliminar"]
    for btn_text in botones:
        # Contenedor para cada boton para alinearlo con los valores de arriba (que tienen padx=10)
        frame_btn_wrapper = tk.Frame(frame_botones, bg=color_primario)
        frame_btn_wrapper.pack(side="left", padx=10, expand=True, fill="x")
        
        btn = tk.Button(frame_btn_wrapper, text=btn_text, font=("Arial", 10, "bold"), bg="white", fg="black", cursor="hand2")
        btn.pack(fill="x")

    # --- Frame Medio (Tabla Debe/Haber) ---
    # Frame contenedor para dar el efecto de borde y footer
    frame_medio = tk.Frame(ventana_info_cliente, bg=color_secundario)
    # Padding inferior grande para simular el footer
    frame_medio.pack(side="top", fill="both", expand=True, padx=20, pady=(10, 30))

    # Treeview
    columns = ("fecha", "detalle", "debe", "haber", "saldo")
    tree = ttk.Treeview(frame_medio, columns=columns, show="headings")
    
    # Estilo para el Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10), rowheight=22)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    tree.heading("fecha", text="Fecha")
    tree.heading("detalle", text="Detalle")
    tree.heading("debe", text="Debe")
    tree.heading("haber", text="Haber")
    tree.heading("saldo", text="Saldo")

    tree.column("fecha", width=100, anchor="center")
    tree.column("detalle", width=350, anchor="w")
    tree.column("debe", width=100, anchor="e")
    tree.column("haber", width=100, anchor="e")
    tree.column("saldo", width=100, anchor="e")

    scrollbar = ttk.Scrollbar(frame_medio, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ventana_info_cliente.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    informacion_cliente()
    root.mainloop()
