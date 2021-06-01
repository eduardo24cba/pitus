from archivos.generador_pedidos import lista_de_pedidos, lista_ids_cliente
from archivos.cambiar_estado_pedidos import cambiar_estado
from archivos.funciones import invertir_fecha, retornar_fuente_responsive, conectar_db, crear_progressbar

import tkinter as tk
from tkinter import messagebox


def crear_lista_pedidos(frame_notebook, frame_tareas, notebook, parent, opcion, ancho_frame_accesos, pedidos_en_proceso=False):
    """
    la opcion puede ser: preparado, en proceso, en camino
    si pedidos_en_proceso es verdadero, retornamos el canvas total pedidos
    """

    #acomodamos todos los widgets al ancho y alto de la resolucion de pantalla actual
    ancho = parent.winfo_width() - ancho_frame_accesos
    alto  = parent.winfo_height()

    frame_tareas.configure(  width=ancho, height=alto)
    frame_notebook.configure(width=ancho, height=alto)
    notebook.configure(      width=ancho, height=alto)

    cursor, database = conectar_db()

    clientes = lista_ids_cliente(opcion, cursor)

    if not clientes:
        messagebox.showinfo("Aviso", "No existen pedidos por preparar")
        database.close()
        return 0


    parent.after(10, lambda:crear_progressbar(frame_notebook, alto, ancho, "red"))

    fuente_responsive = retornar_fuente_responsive(ancho)

    dic_variables = {}

    lista_total_pedidos = []
    
    frame_lista_pedidos = tk.Frame(frame_notebook)

    #crearemos un progressbar que se cargara y dara la impresion de que sigue procesando
    #lo haremos para darle tiempo al programa y a la base de datos
    
    #tk.Button(text="esconder", command=frame_lista_pedidos.grid_forget).grid(row=0, column=0)
    #tk.Button(text="Mostrar", command= lambda: crear_progressbar(frame_notebook, alto, ancho, "#646184")).grid(row=0, column=1)

    frame_lista_pedidos.grid(sticky="nsew")

    frame_total_pedidos = None

    dic_labels = {}


    columna_scroll = 1

    if pedidos_en_proceso:

        columna_scroll = 3

        pedidos_por_preparar = []

        scroll_canvas_total_pedidos = tk.Scrollbar(frame_lista_pedidos, orient=tk.VERTICAL)
        
        canvas_total_pedidos = tk.Canvas(frame_lista_pedidos, bg="yellow" )

        canvas_total_pedidos.configure(yscrollcommand=scroll_canvas_total_pedidos.set)

        scroll_canvas_total_pedidos.config(command=canvas_total_pedidos.yview)

        canvas_total_pedidos.grid(       row=0, column=2, sticky="nsew", padx=5, pady=2)

        lista_total_pedidos.append(canvas_total_pedidos)

        lista_total_pedidos.append(scroll_canvas_total_pedidos)

        lista_final_pedidos = {}
        
        #agregamos las cantidades de cada producto a una sola tabla
        #mostramos la cantidad total de cada producto por el total de los pedidos

        frame_total_pedidos = tk.Frame(canvas_total_pedidos, width=ancho/2, bg="red")
    
        frame_total_pedidos.grid(row=0, column=0, sticky="nsew")

        canvas_total_pedidos.grid_propagate(0)

        #fin pedidos en proceso
        
    scroll_canvas_pedidos = tk.Scrollbar(frame_lista_pedidos, orient=tk.VERTICAL)
    
    canvas_pedidos = tk.Canvas(frame_lista_pedidos, bg="green")

    frame_canvas = tk.Frame(canvas_pedidos, bg="orange")
    
    canvas_pedidos.create_window(0,0, window=frame_canvas, anchor="nw") 

    canvas_pedidos.configure(yscrollcommand=scroll_canvas_pedidos.set)

    scroll_canvas_pedidos.config(command=canvas_pedidos.yview)

    canvas_pedidos.grid(       row=0, column=0,  sticky="nsew", padx=5, pady=2)
    
    scroll_canvas_pedidos.grid(row=0, column=columna_scroll, sticky="nsew", padx=0, pady=2)

    #esta fila arranca en 2 porque va despues de los labels menu y cantidad
    fila = 2

    fila_canvas = 0

    alto_widgets = 0

    lista_frames = []

    ancho_frame_pedidos = 0

    for pedidos in lista_de_pedidos(clientes, opcion, cursor):
        otro_frame = tk.Frame(frame_canvas, bg="yellow")
        otro_frame.grid(row=fila_canvas, column=0, padx=10, pady=4)

        canvas_pedidos.bind("<Button-1>", lambda event:print("Me clikeaste"))

        tk.Label(otro_frame, font=fuente_responsive, text="Numeración/Lote: " + pedidos[-1][2] + " Calle/Manzana: " + pedidos[-1][3]).grid(row=0, column=0, sticky="nsew")
        #tk.Label(otro_frame, text="Fecha %s" % invertir_fecha(pedidos[-1][6], caracter="/")).grid(row=fila, column=1, sticky="nsew")

        tk.Label(otro_frame, font=fuente_responsive, bg="blue", text="Menu").grid(        row=1, column=0, sticky="nsew")
        tk.Label(otro_frame, font=fuente_responsive, bg="blue", text="Cantidad").grid(    row=1, column=1, sticky="nsew")
        #tk.Label(otro_frame, bg="blue", text="Hora").grid(row=fila, column=2, sticky="nsew")
        
        fila_canvas += 1

        lista_frames.append(otro_frame)

        for pedido in pedidos:
            #menu
            label_menu = tk.Label(otro_frame, font=fuente_responsive, bg="blue", text="%s" % pedido[0])
            label_menu.grid(row=fila, column=0, sticky="nsew")
            
            #cantidad
            label_cantidad = tk.Label(otro_frame, font=fuente_responsive, bg="blue", text="%d" % pedido[1])
            label_cantidad.grid(row=fila, column=1, sticky="nsew")
            
            #fecha - hora
            #tk.Label(otro_frame, bg="blue", text="%s" % pedido[7][:5]).grid(row=fila+1, column=2, sticky="nsew")
            
            boton_opcion_1 = tk.Button(otro_frame, font=fuente_responsive)
            boton_opcion_1.grid(row=fila, column=3, sticky="nw")
            
            boton_opcion_2 = tk.Button(otro_frame, font=fuente_responsive)
            boton_opcion_2.grid(row=fila, column=4, sticky="nw")

            #configuramos las funciones de los botones, si no es en puerta es delivery
            if opcion == "en proceso":
                texto = "preparado"
            
            elif opcion == "en camino":
                texto = "despachar"

            else:
                #preparado
                if pedido[5] == "en puerta":
                    texto = "despachar"
                else:
                    texto = "delivery"
            
            boton_opcion_1.configure(text=texto.upper(),
                    command=lambda tipo_entrega = pedido[5], id_pedido = pedido[8], id_cliente = pedido[9], tipo_producto = pedido[0], cantidad_producto=pedido[1],
                    widgets = [label_menu, label_cantidad, boton_opcion_1, boton_opcion_2], frame = otro_frame, menu = pedido[0], precio_menu = pedido[10]
                    :cambiar_estado(id_pedido, texto, widgets, canvas_pedidos, parent, scroll_canvas_pedidos,
                                    tipo_entrega, lista_total_pedidos, id_cliente, lista_frames, frame,
                                    dic_variables, tipo_producto, cantidad_producto, dic_labels, frame_total_pedidos,
                                    frame_notebook, menu, precio_menu))
            
            boton_opcion_2.configure(text="Anular",
                                     command=lambda tipo_entrega = pedido[5], id_pedido = pedido[8], id_cliente = pedido[9], tipo_producto = pedido[0], cantidad_producto=pedido[1],
                                     widgets = [label_menu, label_cantidad, boton_opcion_1, boton_opcion_2], frame = otro_frame, menu = pedido[0], precio_menu = pedido[10]
                                     :cambiar_estado(id_pedido, "anular", widgets, canvas_pedidos, parent, scroll_canvas_pedidos,
                                                     tipo_entrega, lista_total_pedidos, id_cliente, lista_frames, frame,
                                                     dic_variables, tipo_producto, cantidad_producto, dic_labels, frame_total_pedidos,
                                                     frame_notebook, menu, precio_menu))
            
            fila += 1

            if pedidos_en_proceso:
                pedidos_por_preparar.append((pedido[0], pedido[1]))
        
        #reseteamos la fila
        fila = 2
        
        parent.update()
        
        parent.update_idletasks()

        alto_widgets += otro_frame.winfo_height()

        canvas_pedidos.update()

        canvas_pedidos.config(scrollregion=canvas_pedidos.bbox("all"))

        print("el ancho del frame es ", otro_frame.winfo_reqwidth())

        ancho_frame_pedidos = otro_frame.winfo_reqwidth()

    if pedidos_en_proceso:
            
        for pedido in range(len(pedidos_por_preparar)):
            if pedidos_por_preparar[pedido][0] in lista_final_pedidos.keys():
                lista_final_pedidos[pedidos_por_preparar[pedido][0]] = lista_final_pedidos[pedidos_por_preparar[pedido][0]] + pedidos_por_preparar[pedido][1]
            else:
                lista_final_pedidos[pedidos_por_preparar[pedido][0]] = pedidos_por_preparar[pedido][1]

        fila = 0

        for key, value in lista_final_pedidos.items():

            #los nombres no pueden empezar con upper-case letter
            var = tk.IntVar(frame_total_pedidos)
            var.set(value)

            label_descripcion_total_pedidos = tk.Label(frame_total_pedidos, font=fuente_responsive, text="%s" % key)
            label_descripcion_total_pedidos.grid(row=fila, column=0)
                
            label_cantidad_total_pedidos = tk.Label(frame_total_pedidos, font=fuente_responsive, text="%s" % var.get())
            label_cantidad_total_pedidos.grid(row=fila, column=1)

            dic_variables[key] = var

            dic_labels[key] = [label_descripcion_total_pedidos, label_cantidad_total_pedidos]

            fila += 1


    if pedidos_en_proceso:
        canvas_pedidos.configure(      width=ancho_frame_pedidos, height=alto)
        ancho_total_pedidos = ancho - ancho_frame_pedidos

        canvas_total_pedidos.configure(width=ancho_total_pedidos, height=alto)
    else:
        canvas_pedidos.configure(width=ancho, height=alto)
        


    #parent.after(10000, frame_lista_pedidos.grid_forget())
    #parent.after(12000, frame_lista_pedidos.grid_forget())
    if alto_widgets < canvas_pedidos.winfo_height():
        scroll_canvas_pedidos.grid_forget()
    else:
        pass

    database.close()

    print("termino la lista generar pedidos")