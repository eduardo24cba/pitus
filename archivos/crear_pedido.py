import tkinter as tk
import time
import traceback

from tkinter import messagebox
from tkinter import ttk

from archivos.funciones import marcar_activo, conectar_db, extraer_id, obtener_fecha, retornar_fuente_responsive, desactivar_activar_tabs, crear_progressbar
from archivos.constantes import BG_BOTONES, ENVIO, PRECIO_TOTAL, NOMBRE_CLIENTE
from archivos.multibox import MultiListbox
from archivos.entrega import verificar_envio, cambiar_entrega


#si elegimos un cliente y cambiamos de pestaña
#cuando volvemos y queremos elegir un cliente nos informa que ya hay un cliente
#debemos setear todas la variables cuando salgamos de la pestaña crear pedido

def interfaz_crear_pedido(parent, frame_pedidos, boton,  botones, clase_cliente,
                          clase_producto, clase_envio, notebook, ancho_frame_accesos,
                          frame_tareas):
    # establecemos el alto, ancho del frame haciendolo responsive

    #print("el ancho de la pantalla es ahora", parent.winfo_width())

    ancho = parent.winfo_width() - ancho_frame_accesos
    alto  = parent.winfo_height()

    parent.after(10, lambda:crear_progressbar(frame_pedidos, alto, ancho, "red"))

    fuente_responsive = retornar_fuente_responsive(ancho)

    frame_tareas.configure(width=ancho, height=alto)
    frame_pedidos.configure(width=ancho, height=alto)
    notebook.configure(width=ancho, height=alto)


    if boton:
        marcar_activo(boton, botones)

    fg_boton = '#d7d7d7'

    parent.update()

    frame_nuevo_pedido = tk.Frame(frame_pedidos, width=ancho, height=alto)

    frame_nuevo_pedido.grid()

    # variables que se pasan a los botones
    opcion_entrega = tk.StringVar(parent)
    var_cargoenvio = tk.IntVar(parent)
    precio_total = tk.IntVar(parent)
    total_envio = tk.IntVar(parent)
    total = tk.IntVar(parent)

    # el precio actual del pedido siempre comienza en 0

    # que afecataran al total de la venta

    # por defecto, siempre sera 0, se valida en guardar pedido
    precio_total.set(0)
    var_cargoenvio.set(0)
    total_envio.set(0)

    total.set(0)

    #esta database se cierra desde cargo envio
    cursor, database = conectar_db()

    lista_clientes = cursor.execute(
        "SELECT NUMERACIONOLOTE, CALLEOMANZANA, TELEFONO, BARRIO, ROWID FROM CLIENTE ORDER BY NUMERACIONOLOTE ASC")

    lista_clientes = lista_clientes.fetchall()

    database.close()

    

    # para ajustar los frames a cualquier resolucion

    # ¡verificar este ancho en diferentes resoluciones!


    #verificar esta bosta del ancho, no entiendo por que no funciona igual en todos lados, verificar funcion 
    ancho_frames = ancho - 200
    alto_frame_bottom = 80
    alto_frames = alto - alto_frame_bottom
    ancho_frame_opciones = 140

    # los tres frames principales
    frame_opciones = tk.Frame(
        frame_nuevo_pedido, bg="#3065AC", bd=1, relief=tk.FLAT)

    frame_factura = tk.Frame(frame_nuevo_pedido, bg="#FF6961", bd=1, relief=tk.FLAT)
    
    frame_bottom = tk.Frame(frame_nuevo_pedido, bg="#BDECB6",  bd=1, relief=tk.FLAT)
    
    #--labels
    label_precio_total = tk.Label(frame_bottom, font=fuente_responsive, text=PRECIO_TOTAL % precio_total.get())

    label_nombre_cliente = tk.Label(frame_factura, font=fuente_responsive, text=NOMBRE_CLIENTE)

    label_cargo_envio = tk.Label(frame_factura, font=fuente_responsive, text=ENVIO % 0)

    #--envio 

    boton_cargo_envio = tk.Button(frame_bottom, font=fuente_responsive, bg=BG_BOTONES,
                                  activebackground=BG_BOTONES, fg=fg_boton,
                                  text="Cargo de envío")

    #--productos
    menu = tk.Button(frame_opciones, font=fuente_responsive, bg=BG_BOTONES, fg=fg_boton, text="Menu")

    guarnicion = tk.Button(frame_opciones, font=fuente_responsive, bg=BG_BOTONES, fg=fg_boton, text="Guarnicion")

    bebidas = tk.Button(frame_opciones, font=fuente_responsive, bg=BG_BOTONES, fg=fg_boton, text="Bebida")

    postres = tk.Button(frame_opciones, font=fuente_responsive, bg=BG_BOTONES, fg=fg_boton, text="Postre")

    agregar_producto = tk.Button(frame_opciones, text="Agregar Producto", bg=BG_BOTONES, activebackground=BG_BOTONES,
                                 fg=fg_boton, font=fuente_responsive)

    #--cliente
    boton_buscar_cliente = tk.Button(frame_opciones, font=fuente_responsive, bg=BG_BOTONES, fg=fg_boton, text="Buscar cliente")

    boton_agregar_cliente = tk.Button(frame_opciones, text="Agregar Cliente", font=fuente_responsive,
                                     bg=BG_BOTONES, activebackground=BG_BOTONES, fg=fg_boton)

    #--opciones de entrega
    boton_retira_delivery = tk.Radiobutton(frame_bottom, value="delivery", text="Delivery", bg=BG_BOTONES, activebackground=BG_BOTONES,
                                           fg=fg_boton, variable=opcion_entrega, font=fuente_responsive, indicatoron=0, selectcolor=BG_BOTONES)

    boton_retira_puerta = tk.Radiobutton(frame_bottom, value="en puerta", text="En puerta", bg=BG_BOTONES, activebackground=BG_BOTONES,
                                         fg=fg_boton, variable=opcion_entrega, font=fuente_responsive, indicatoron=0, selectcolor=BG_BOTONES)

    #--opciones de transaccion
    cancelar = tk.Button(frame_bottom, font=fuente_responsive,
                         bg=BG_BOTONES, fg=fg_boton, text="Cancelar")

    guardar = tk.Button(frame_bottom, font=fuente_responsive,
                        bg=BG_BOTONES, fg=fg_boton, text="Guardar")

    parent.update()
    parent.update_idletasks()

    frame_opciones.update()

    #al ancho mas grande que tienen los botones de acuerdo a su texto
    ancho_frames = ancho - (agregar_producto.winfo_reqwidth() + 20)

    #print("el porcentaje que ocupa es: ", agregar_producto.winfo_reqwidth()/ancho * 100)

    parent.after(50, lambda: frame_factura.configure(height=alto_frames, width=ancho_frames ))
    parent.after(50, lambda: frame_bottom.configure( height=alto_frame_bottom, width=ancho_frames ))

    #--factura
    factura = MultiListbox(frame_factura,
                           (('Descripcion', 15), ('Cantidad', 5),
                            ('Precio Unit.', 5), ('Monto', 5)),
                           bg="#FDFD96", alineacion="nw", factura=True,
                           font=fuente_responsive)

    #--asignamos las referencias a las variables de cada clase

    #cliente
    clase_cliente.lista = lista_clientes
    clase_cliente.fuente = fuente_responsive
    clase_cliente.label_cliente = label_nombre_cliente
    clase_cliente.label_envio = label_cargo_envio
    clase_cliente.var_envio = var_cargoenvio
    clase_cliente.precio_actual = precio_total
    clase_cliente.label_precio_total = label_precio_total
    clase_cliente.total_envio = total_envio

    #producto
    clase_producto.factura = factura
    clase_producto.var_precio_total = precio_total
    clase_producto.label_precio_total = label_precio_total
    
    #envio
    clase_envio.id_cargoenvio = var_cargoenvio
    clase_envio.parent = parent
    clase_envio.label_envio = label_cargo_envio
    clase_envio.label_precio_total = label_precio_total
    clase_envio.var_precio_total = precio_total
    clase_envio.total_envio = total_envio
    clase_envio.id_cliente = clase_cliente.id_cliente
    clase_envio.entrega = opcion_entrega
    
    #--asignamos los command a los botones
    boton_cargo_envio.configure(command=clase_envio.opciones_envio)
    
    #_opciones_productos
    menu.configure(      command=lambda: clase_producto.ventana_producto("menu"))
    guarnicion.configure(command=lambda: clase_producto.ventana_producto("guarnicion"))
    bebidas.configure(   command=lambda: clase_producto.ventana_producto("bebida"))
    postres.configure(   command=lambda: clase_producto.ventana_producto("postre"))
    agregar_producto.configure(command=clase_producto.ventana_agregar_producto)

    #_opciones_cliente
    boton_buscar_cliente.configure(command=clase_cliente.buscar_cliente)
    boton_agregar_cliente.configure(command=lambda desde_fuera=True: clase_cliente.crear_cliente(main_ventana=parent, desde_fuera=desde_fuera))

    #_transaccion
    guardar.configure(command=lambda: guardar_pedido(factura,
                      clase_cliente, var_cargoenvio, opcion_entrega, label_nombre_cliente, label_precio_total,
                      label_cargo_envio, var_cargoenvio, parent, precio_total, total_envio, clase_producto,
                      clase_envio, notebook))
    
    
    
    # frame factura
    label_nombre_cliente.grid(row=0, column=1, sticky="nw")
    label_cargo_envio.grid(row=1, column=1, sticky="nw")
    factura.grid(row=2, column=0, sticky="nsew",
                 pady=10, padx=2, columnspan=10)

    # frame opciones
    menu.grid(      row=0, column=0, sticky="nsew", pady=2)
    guarnicion.grid(row=1, column=0, sticky="nsew", pady=2)
    
    bebidas.grid(row=2, column=0, sticky="nsew", pady=2)
    postres.grid(row=3, column=0, sticky="nsew", pady=2)
    
    agregar_producto.grid(row=4, column=0, sticky="nsew", pady=2)

    boton_buscar_cliente.grid( row=5, column=0, sticky="nsew", pady=2)
    boton_agregar_cliente.grid(row=6, column=0, sticky="nsew", pady=2)

    # frame bottom
    boton_retira_delivery.grid(row=0, column=0, sticky="nsew", padx=4)
    boton_retira_puerta.grid(  row=0, column=1, sticky="nsew", padx=4)
    
    cancelar.grid(row=0, column=2, sticky="nsew", padx=4)
    guardar.grid( row=0, column=3, sticky="nsew", padx=4)
    
    #boton_descuento.grid(row=0, column=4, sticky="nsew", padx=4)
    boton_cargo_envio.grid( row=0, column=5, sticky="nsew", padx=4)
    label_precio_total.grid(row=0, column=7, sticky="nsew", padx=4)

    #frames principales
    frame_opciones.grid(row=0, column=0, sticky="nsew", pady=2, padx=5)
    frame_factura.grid( row=0, column=1, sticky="nsew", pady=2)
    frame_bottom.grid(  row=1, column=1, sticky="nsew", pady=2)

    #debemos aplicar grid_propagate(0) para que el frame conserve el ancho y el alto.
    frame_factura.grid_propagate(0)
    frame_bottom.grid_propagate(0)

    #no se aplica propagate a este frame para que sea el boton quien decida el ancho
    #frame_opciones.grid_propagate(0)

    # colocamos configure de esta forma para poder alinear el label nombre cliente y la factura
    frame_factura.columnconfigure( 0, weight=0)
    frame_factura.columnconfigure( 1, weight=1)
    frame_opciones.columnconfigure(0, weight=1)

    #le damos el mismo espacio a todos los botones 
    frame_bottom.columnconfigure(0, weight=5)
    frame_bottom.columnconfigure(1, weight=5)
    frame_bottom.columnconfigure(2, weight=5)
    frame_bottom.columnconfigure(3, weight=5)
    frame_bottom.columnconfigure(4, weight=1)
    frame_bottom.columnconfigure(5, weight=1)
    frame_bottom.columnconfigure(7, weight=1)


    #print("el ancho frame opciones es ", ancho_frame_opciones)

    frame_nuevo_pedido.grid_propagate(0)

    parent.update()

    #parent.after(50, lambda:print(guardar.winfo_height()))

    #frame_bottom.grid_rowconfigure(  1, weight=1)
    # self.frame_auxiliar

    print("##############termine")

def guardar_pedido(factura, clase_cliente, var_cargo_envio, opcion_entrega, label_nombre_cliente, 
                   label_precio_total, label_cargo_envio, var_cargoenvio, parent, precio_total,
                   total_envio, clase_producto, clase_envio, notebook):
    #var_cargoenvio, parent, precio_actual, total_envio seran enviados en la funcion opciones_envio 
    #cuando el usuario presione la opcion si en el cuadro de dialogo

    realizo_pedidos = False

    cursor, database = conectar_db()
    
    productos = []

    if obtener_fecha(fecha=True):
        fecha_creacion = obtener_fecha(fecha=True)
    else:
        messagebox.showerror(messagebox.ERROR, "No se ha podido obtener la fecha")
        return 0

    #El estado siempre sera en proceso
    estado = "en proceso"
    hora_creacion = time.strftime("%I:%M:%S")
    descuento = 0

    #factura donde se agregaron los productos
    if not factura.size():#esta vacia
        messagebox.showerror(messagebox.ERROR, "Debes seleccionar al menos 1 producto")
        return 0
    else:
        #el primer item de la factura es el nombre del producto que es la llave de alguno de los dict.
        pass
            
    #cliente 
    if not clase_cliente.id_cliente.get():
        messagebox.showerror(messagebox.ERROR, "Debes seleccionar un cliente")
        return 0
    else:
        #el cliente realizo otros pedidos?
        if consultar_pedidos_cliente(clase_cliente.id_cliente.get(), cursor):
            realizo_pedidos = True

    #delivery o en puerta
    if not opcion_entrega.get():
        messagebox.showerror(messagebox.ERROR, "Selecciona una opción de entrega para el pedido.")
        return 0
    else:
        #si la entrega es igual a la que tienen los pedidos anteriores
        #seteamos la variable a 1 indicando que ya paso por aca.
        if realizo_pedidos:
            if verificar_envio(clase_cliente.id_cliente.get(), opcion_entrega.get(), cursor):
                pass
            else:
                consulta = messagebox.askyesno(messagebox.QUESTION,
                "El cliente tiene seleccionada una opcion de entrega diferente para los pedidos\n ¿Desea cambiar la entrega para todos los pedidos de este cliente?")
                        
                if consulta:
                    cambiar_entrega(clase_cliente.id_cliente.get(), opcion_entrega.get(), cursor)
                    return
                else:
                    messagebox.showerror("Error", "Lo sentimos, todos los pedidos deben tener la misma opción de entrega.\nPor favor, modificala.")
                    return 0

    #cargo de envio
    if opcion_entrega.get() != "en puerta":
        # si la opcion es en puerta no puede aplicar cargo de envio
        # verificar eso

        if var_cargo_envio.get():
            #selecciono un cargo de envio, entonces lo establecemos.
            #no se aplica un commit, sino se ha insertado el o los pedidos.
            resultado = clase_envio.aplicar_o_quitar_envio_a_cliente(cursor=cursor)
            if not resultado:
                return 0
        
        else:
            consulta = messagebox.askyesno(messagebox.QUESTION, "No aplico ningún cargo de envío ¿Desea aplicar?")
            if consulta:
                clase_envio.opciones_envio()
                return 0

    valores = ""

    operacion = "INSERT INTO PEDIDO (idPRODUCTO, CANTIDADPRODUCTO, idCLIENTE, ESTADO, TIPOENTREGA, idDESCUENTO, FECHA, HORACREACION) VALUES"

    #pasamos el id del menu seleccionado y armamos la tupla con los datos restantes para guardar en la base de datos
    #idProducto, cantidadproducto, idCLiente, estado, entrega, descuento, fechaCreacion, horaCreacion.
    for item in range(factura.size()):

        valor = (extraer_id((clase_producto.dic_menu, clase_producto.dic_guarnicion,
                 clase_producto.dic_bebida, clase_producto.dic_postre), factura.get(item)[0]),
                 factura.get(item)[1], clase_cliente.id_cliente.get(),
                 estado, opcion_entrega.get(), descuento, fecha_creacion, hora_creacion)
        
        valor = str(valor) + ","
        
        valores += valor

    #eliminamos la ultima coma y agregamos el ;
    valores = valores[:-1] + ";"

    if cursor:
        try:
            cursor.execute(operacion + valores)
            
            cursor.connection.commit()
        except Exception:
            messagebox.showerror(messagebox.ERROR, "Excepcion al guardar el pedido %s" % traceback.format_exc())
            return 0

        except database.Error:
            messagebox.showerror(messagebox.ERROR, "Excepcion al guardar el pedido %s" % traceback.format_exc())
            return 0

        else:
            messagebox.showinfo(messagebox.ERROR, "Pedido guardado con exito")
            #borramos todo de la listbox
            factura.delete(0, tk.END)

            #reseteamos las variables
            var_cargo_envio.set(0)
            opcion_entrega.set("")
            precio_total.set(0)
            
            #borramos los labels que tenemos
            label_nombre_cliente.config(text=NOMBRE_CLIENTE)
            label_precio_total.config(text=PRECIO_TOTAL % 0)
            label_cargo_envio.config(text=ENVIO % 0)

            #reseteamos las variables que vienen desde menu principal
            clase_producto.producto_seleccionado.set(0)
            clase_cliente.id_cliente.set(0)

            desactivar_activar_tabs(notebook, False)

            return

        finally:
            database.close()
            
    else:
        messagebox.showerror(messagebox.ERROR, "No se pudo conectar a la base de datos")
        return 0
    
def consultar_pedidos_cliente(id_cliente, cursor):
    consulta = cursor.execute("SELECT * FROM PEDIDO WHERE idCLIENTE='%d' AND ESTADO NOT LIKE 'Despachado'" % id_cliente)
    
    consulta = consulta.fetchone()

    if consulta:
        #el cliente realizo pedidos
        print(consulta)
        return 1
    else:
        #no realizo ningun pedido todavia o los pedidos estan despachados
        print("no realizo pedidos")
        return 0
