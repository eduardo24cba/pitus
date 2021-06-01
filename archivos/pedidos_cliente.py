def pedidos_en_proceso(self, opcion, parent):
        """Dependiendo que opcion tengamos
           mostraremos diferentes estados
           opcion 1:En proceso
           opcion 2:Delivery
           opcion 3:despachados
           """

        #se le da un efecto sombra a las comandas
        #el truco esta en posicionar un label arriba de otro frame
        #dandoles el mismo ancho pero diferenciandolos en los pady y padx
        #frame es igual a padx=(x,x) pady=(x,x) y label es igual a padx=(0,x) pady=(0,x)
            
        cursor,database = conectar_db()
        #opcion, delivery - en puerta.
        boton_opcion = None

        if opcion == "En proceso":
            opciones = ("En proceso", "Preparado")

        else:
            opciones = ("En camino", "En camino")
        
        #consulta[item][10] si es delivery color verde, si es en puerta azul
        color = None
        
        if cursor and database:
            try:
                consulta = cursor.execute("""SELECT c.LOTE, c.MANZANA,
                pe.idPEDIDO, pe.idCLIENTE, pe.ENTREGA FROM PEDIDO pe, CLIENTE c 
                WHERE pe.idCLIENTE = c.idCLIENTE AND pe.ESTADO IN('%s','%s') """ % opciones)
                consulta = consulta.fetchall()
            except db.Error:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            else:
                database.close()
                
            clientes = []
            for x in consulta:
                if not x[3] in clientes:
                    clientes.append(x[3])

            row = 0
            column = 0
            
            if consulta:
                #creamos la ventana
                #se utiliza canvas para poder agregar varios frames
                #y que estos esten sujetos a un scroll
                if not self.comprobar(self.frame_auxiliar):
                    self.frame_auxiliar = Frame(parent)
                else:
                    self.frame_auxiliar = Frame(parent)

                alto,ancho = widget_responsive(self, 70, 145)
                ancho_boton = ancho / 3
                ancho_boton = ancho_boton / 10 #disminuimos la escala
                ancho_boton = int(ancho_boton) - 3 #se le resta el margen que se le dara

                #label info
                if opcion == "En proceso":
                    Label(parent, font=fuente_wid, bg=BG_COMANDA_ENTREGA, width=16, text="Retiran en puerta").grid(row=0,
                          column=0, padx=2, pady=2, sticky="nw")
                    Label(parent, font=fuente_wid, bg=BG_COMANDA_DELIVERY, width=16, text="Delivery").grid(row=0,
                          column=1, padx=2, pady=2, sticky="nw")
                    self.frame_auxiliar.grid(row=2, column=0, padx=0, pady=2, columnspan=20)
                else:
                    self.frame_auxiliar.grid(row=2, column=0, padx=0, pady=30, columnspan=4)
                #self.frame_ventanas.config(bg=fondo, relief=SUNKEN)
                
                scroll = Scrollbar(self.frame_auxiliar)
                canvas = Canvas(self.frame_auxiliar, yscrollcommand=scroll.set, width=ancho, height=alto, bg=BG_PEDIDOS)
                scroll.config(command=canvas.yview)
                scroll.pack(side=RIGHT, fill=Y)
                canvas.pack(expand=True, fill=BOTH)
                
                frame_labels = Frame(canvas, bg=BG_PEDIDOS)
                #crea la magia, en las coordenadas que le indiquemos
                #creara nuevos frames
                canvas.create_window(0, 0, window=frame_labels)

                #definimos un contador que nos sirve para saber si es el mismo cliente
                #si es el mismo cliente, se borra de la lista y el indice queda igual
                #si no es el mismo cliente, entonces vamos a la siguiente posicion
                #damos un maximo de 3 botones por fila
                #agregar image=self.imagen_comanda, compound=CENTER

                for x in range(len(clientes)):
                    count = 0
                    cantidad_pedidos = 0
                    frame_labels_frame = Frame(frame_labels, bg=BG_PEDIDOS)
                    pedido = Label(frame_labels_frame, width=ancho_boton, height=6, font=fuente_wid, )
                    for y in consulta[:]:#accedemos a una copia de la lista
                        if consulta[count][3] == clientes[x]:
                            if y[4] == "Delivery":
                                color = BG_COMANDA_DELIVERY
                            else:
                                color = BG_COMANDA_ENTREGA
                            cantidad_pedidos+=1
                            pedido.config(text=TEXTO_COMANDA % (y[0],y[1],cantidad_pedidos),
                                          bg=color)
                            
                            #pasamos el event que es el label presionado, nombre, apellido y la cantidad de pedidos
                            #se reemplaza button por label, bind funciona mejor que command
                            pedido.bind("<Button-1>", lambda event, cliente = clientes[x],
                                          estado=opcion, frame=frame_labels_frame, comanda=pedido,
                                          nombre=y[0], apellido=y[1]:
                                          self.mostrar_pedidos_cliente(id_cliente=cliente,
                                                                       estado=estado,
                                                                       frame=frame,
                                                                       canvas=canvas,
                                                                       comanda=comanda,
                                                                       boton_comanda=[event,nombre,apellido]))
                            del consulta[count]
                        else:
                            count+=1
                    if x % 3 == 0 and x != 0:
                        row+=1
                        column=0

                    column+=1
                    pedido.grid(pady=(0,2), padx=(0,2))
                    frame_labels_frame.grid(row=row, column=column, pady=10, padx=10)
                    self.update()
                    canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(0)#ubicamos el scroll arriba
            else:
                messagebox.showinfo(title="Sin pedidos", message="No existen pedidos")
                return 0
        
    def mostrar_pedidos_cliente(self, id_cliente, estado, frame, canvas, comanda, boton_comanda):
        #boton_comanda = los datos de la comanda, nombre-apellido-cantidad pedidos

        

        cursor, database = conectar_db()
        
        if cursor and database:
            try:
                if estado != "En camino":
                    datos = (id_cliente, estado, "Preparado")
                else:
                    datos = (id_cliente, estado, estado)

                consulta = self.consulta_pedidos(cursor, datos)
                
                consulta = consulta.fetchall()

                consulta_envio = cursor.execute("""SELECT cr.PRECIO FROM CLIENTE cl
                                                             INNER JOIN CARGOENVIO cr ON cl.idCARGOENVIO = cr.idCARGOENVIO
                                                             WHERE cl.idCLIENTE='%d'""" % id_cliente)
                consulta_envio = consulta_envio.fetchone()
                precio_total = 0

                if consulta:

                    frame_comanda = frame
                    canvas_comanda= canvas

                    nueva_ventana    = crear_ventana(self, resizable=True)
                        
                    alto, ancho = widget_responsive(self, 110, 130)
                    
                    scroll = Scrollbar(nueva_ventana)
                    canvas = Canvas(nueva_ventana, width=ancho, height=alto, yscrollcommand=scroll.set, bg=BG_PEDIDOS)
                    scroll.config(command=canvas.yview)
                    scroll.grid(row=0, column=1, sticky="nsew")
                    canvas.grid(row=0, column=0, sticky="nsew")

                    frame_labels = Frame(canvas, bg=BG_PEDIDOS)
                    
                    #crea la magia, en las coordenadas que le indiquemos
                    #creara nuevos frames
                    var_estado_entrega = StringVar(frame_labels)

                    ancho = ancho / 10
                    ancho = int(ancho)
                    
                    
                    canvas.create_window(0, 0, window=frame_labels, anchor="nw")

                    #la cantidad de frames que tiene canvas
                    self.cantidad_widget = len(consulta)
                
                    #fecha y hora
                    Label(frame_labels, font=fuente_wid, relief=GROOVE, bd=2, bg=BG_FRAMES,
                          fg='#d7d7d7', text="Fecha: %s Hora: %s" % (invertir_fecha(consulta[0][17]), consulta[0][18]),
                          justify=LEFT, anchor=W).grid(row=0, column=0, columnspan=2, sticky="nsew")
                    #estado
                    Label(frame_labels, font=fuente_wid, relief=GROOVE, bd=2, bg=BG_FRAMES,
                          fg='#d7d7d7', text="Estado: %s" % consulta[0][16],
                          justify=LEFT, anchor=W).grid(row=1, column=0, columnspan=2, sticky="nsew")
                    #entrega
                    Label(frame_labels, font=fuente_wid, relief=GROOVE, bd=2, bg=BG_FRAMES, fg='#d7d7d7',
                          text="Entrega: %s" % consulta[0][19],
                          justify=LEFT, anchor=W).grid(row=2, column=0, columnspan=2, sticky="nsew")
                    #datos
                    Label(frame_labels, font=fuente_wid, relief=GROOVE, bd=2, bg=BG_FRAMES, fg='#d7d7d7',
                          text="Lote: %s\nManzana: %s\nTelefono: %s\nBarrio: %s\n" % consulta[0][12:16],
                          justify=LEFT, anchor=W).grid(row=3, column=0, columnspan=2, sticky="nsew")
                    #label_precio
                    frame_ = Frame(frame_labels, bg=BG_FRAMES, relief=GROOVE, bd=2)
                    
                    precio = Label(frame_, text="Precio Total: $", font=fuente_wid, bg=BG_FRAMES, justify=LEFT, anchor=W)
                    precio.grid(row=1, column=0, sticky="ne")
                    #total 
                    label_total = Label(frame_, font=fuente_wid, bg=BG_FRAMES, justify=LEFT, anchor=W)

                    label_total.grid(row=1, column=1, sticky="nw")

                    label_descuento = Label(frame_, font=fuente_wid, bg=BG_FRAMES,
                                   justify=LEFT, anchor=W)
                    label_descuento.grid(row=2, column=0, sticky="nsew", columnspan=2)

                    label_envio = Label(frame_, font=fuente_wid, bg=BG_FRAMES,
                                   justify=LEFT, anchor=W)
                    label_envio.grid(row=1, column=3, sticky="nsew", columnspan=2)

                    #Label(frame_, bg=BG_FRAMES, font=fuente_botones,
                    #      text=u"El cargo de envío se suma al precio total de los pedidos",
                    #      justify=LEFT, anchor=W).grid(row=3, column=0, sticky="nsew", columnspan=4)

                    frame_.grid(row=4, column=0, columnspan=2, sticky="nsew")
                    
                    nueva_ventana.title(u"Visualización de pedido. Cliente: %s %s" % (consulta[0][16], consulta[0][17]))

                    #si nos encontramos en delivery, significa que el pedido ya salio
                    #no deberia poder modificarse la entrega ni el pedido
                    
                    if estado != "En camino":
                        Button(frame_labels, text='Cambiar entrega de los pedidos',
                               bg=BG_BOTONES,
                               activebackground=BG_BOTONES,
                               command=lambda id_cliente=consulta[0][22],
                               entrega=consulta[0][19],
                               cantidad=len(consulta),
                               parent=self,
                               font=fuente_wid,
                               ventana=nueva_ventana,
                               datos_cliente=(consulta[0][12],consulta[0][13]):
                               cambiar_entrega(parent, id_cliente, entrega,
                                               cantidad, ventana, datos_cliente,
                                               comanda)).grid(pady=10, sticky="nw")

                    if consulta[0][19] == "Delivery" and estado != "En camino":
                        Button(frame_labels, text="En camino",
                               bg=BG_BOTONES,
                               activebackground=BG_BOTONES,
                               command=lambda:
                               self.verificar_estado_delivery(id_cliente=id_cliente, ventana=nueva_ventana,
                                                              frame_comanda=frame_comanda)).grid(pady=10, sticky="nw")

                    #al ser una tupla, siempre entrara al if
                    #evitamos escribir cargo de envio si no hay.
                    try:
                        cargo_envio  = consulta_envio[0]
                    except:
                        cargo_envio  = consulta_envio

                    #si un pedido tiene envio o descuento, los demas tambien
                    #evitamos reescribir el label en el for
                    if consulta[0][30]:
                        label_descuento.config(text=DESCUENTO %  consulta[0][30])

                    if cargo_envio:
                        label_envio.config(text=ENVIO % cargo_envio)
                    else:
                        if consulta[0][19] == "Delivery":
                            Button(frame_labels, text="Agregar cargo de envío",
                                   bg=BG_BOTONES,
                                   activebackground=BG_BOTONES,
                                   command=lambda:aplicar_envio(id_cliente, label_envio)
                                   ).grid(pady=10, sticky="nw")
                            
                    for item in range(len(consulta)):
                        total_pedido = consulta[item][20]

                        descuento = consulta[0][30]
                        
                        #los datos para modificar el pedido
                        #Menu, cantidad menu
                        #Guarnicion, cantidad guarnicion
                        #Postre, cantidad postre
                        #Bebida, cantidad bebida
                        #cliente, entrega,
                        #id_pedido,
                        #precio guarnicion
                        #promo, cantidad promo
                        #descuento, cargo de envio
                        
                        datos = [consulta[item][0], consulta[item][1],
                                 consulta[item][3], consulta[item][4],
                                 consulta[item][9], consulta[item][10],
                                 consulta[item][6], consulta[item][7],
                                 consulta[item][22],consulta[item][19],
                                 consulta[item][21],consulta[item][5],
                                 consulta[item][27],consulta[item][28],
                                 descuento, cargo_envio]

                        precio_total = precio_total + consulta[item][20] 

                        #si un pedido tiene descuento, los demas tambien
                        #no debe existir un pedido con descuento y otro no.
                        if descuento:
                            
                            descuento = round((consulta[item][20] * descuento) / 100)
                            total_pedido = total_pedido - descuento
                            precio_total = precio_total - descuento


                        frame_labels_frame = Frame(frame_labels, bd=5, relief=GROOVE, bg=BG_PEDIDO_PED_PREPA, width=100)
                        menu = Frame(frame_labels_frame)

                        #segun el producto que haya, se agrega
                        #si la cantidad del producto es >1
                        ##menu
                        if consulta[item][1]:
                            Label(menu, text=u"Menú: %s\nCantidad: %d\nPrecio unitario: $%d" % consulta[item][:3],
                                  width=ancho-10, bg=BG_PEDIDO_PED_PREPA,
                                  justify=LEFT, anchor="nw", font=fuente_wid).grid(sticky="nsew")
                        ##guarncion
                        if consulta[item][4]:
                            Label(menu, text=u"Guarnición: %s\nCantidad: %d\nPrecio unitario: $%d" % consulta[item][3:6],
                                  width=ancho-10, bg=BG_PEDIDO_PED_PREPA,
                                  justify=LEFT, anchor="nw", font=fuente_wid).grid(sticky="nsew")
                        ##postre
                        if consulta[item][10]:
                            Label(menu, text=u"Postre: %s\nCantidad: %d\nPrecio unitario: $%d" % consulta[item][9:12],
                                  width=ancho-10, bg=BG_PEDIDO_PED_PREPA,
                                  justify=LEFT, anchor="nw", font=fuente_wid).grid(sticky="nsew")
                        ##bebida
                        if consulta[item][7]:
                            Label(menu, text=u"Bebida: %s\nCantidad: %d\nPrecio unitario: $%d" % consulta[item][6:9],
                                  width=ancho-10, bg=BG_PEDIDO_PED_PREPA,
                                  justify=LEFT, anchor="nw", font=fuente_wid).grid(sticky="nsew")
                        ##promo
                        if consulta[item][28]:
                            Label(menu, text=u"Promoción: %s\nCantidad: %d\nPrecio unitario: $%d" % consulta[item][27:30],
                                  width=ancho-10, bg=BG_PEDIDO_PED_PREPA,
                                  justify=LEFT, anchor="nw", font=fuente_wid).grid(sticky="nsew")

                        menu.grid(row=item + 1, column=0, columnspan=20, sticky="nsew")

                        Label(frame_labels_frame, text=u"Total del pedido: $%d" % total_pedido,
                              bg=BG_PEDIDO_PED_PREPA, justify=LEFT, anchor="nw",
                              font=fuente_wid).grid(row=item + 2, column=0, sticky="nsew")

                        #Despachar o Preparado para que lo lleve el delivery
                        #si los pedidos ya estan preparados, daremos esa impresion con el borde del label
                        boton_opcion = Label(frame_labels_frame, bg=BG_BOTONES, activebackground=BG_BOTONES,
                                             relief=SUNKEN if consulta[item][31] == "Preparado" else RAISED)
                        boton_opcion.bind('<Button-1>', lambda event,
                                          ventana=nueva_ventana,
                                          frame = frame_labels_frame,
                                          id_pedido=consulta[item][21],
                                          texto=var_estado_entrega,
                                          b_comanda = boton_comanda,
                                          total=total_pedido,
                                          label_precio = label_total:
                                          self.cambiar_estado(ventana,
                                                              frame, canvas,
                                                              id_pedido, texto,
                                                              b_comanda,
                                                              frame_comanda,
                                                              canvas_comanda,
                                                              total,
                                                              label_precio,
                                                              event,
                                                              cargo_envio,
                                                              id_cliente))

                        #anular pedido
                        Button(frame_labels_frame, textvariable=self.anular_pedido,
                               bg=BG_BOTONES,
                               activebackground=BG_BOTONES,
                               command=lambda ventana=nueva_ventana, 
                               frame = frame_labels_frame,
                               id_pedido=consulta[item][21],
                               texto=self.anular_pedido,
                               b_comanda = boton_comanda:
                               self.cambiar_estado(ventana,
                                                   frame, canvas,
                                                   id_pedido, texto,
                                                   b_comanda,
                                                   frame_comanda,
                                                   canvas_comanda)).grid(row=item + 2, column=17, sticky="nsew")

                        #dependiendo el estado de la entrega, pondremos un texto diferente
                        if consulta[item][19] == "Delivery" and estado != "En camino":
                            var_estado_entrega.set("Preparado")
                            boton_opcion.config(text="Preparado")
                        else:
                            var_estado_entrega.set("Despachar")
                            boton_opcion.config(text="Despachar")
                            
                        if estado != "En camino":
                            Button(frame_labels_frame, text='Modificar pedido', bg=BG_BOTONES, activebackground=BG_BOTONES,
                               command=lambda v=nueva_ventana, d=datos :self.modificar_pedido(v,d)).grid(row=item + 2, column=18, sticky="nsew")


                        frame_labels_frame.grid(pady=10, padx=20, columnspan=20)
                        boton_opcion.grid(row=item + 2, column=19, sticky="nsew")
                        self.update()
                        canvas.config(scrollregion=canvas.bbox("all"))

                    
                    label_total.config(text="%d" % precio_total)

                    canvas.yview_moveto(0)
                    centrar(nueva_ventana)
                
            except db.Error:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            else:
                database.close()


def cambiar_estado(self, ventana, frame, canvas, id_pedido, texto,
                       datos_comanda, frame_comanda=None, canvas_comanda=None,
                       total=None, label_precio=None, boton_opcion=None,
                       cargo_envio=None, id_cliente=None):
        #si el estado es despachar, entonces sacaremos el total de ese pedido
        #y lo sumaremos a la caja. Nuestra primera venta.
        #seteamos las opciones, para ser mas legible a la hora de filtrar.
        #id= id_pedido
        #self.cantidad_widget siempre tomara el total de la consulta
        #de pedidos de cliente, cambiar estado siempre estara asociado a este listado

        #los datos de la comanda, para actualizar la cantidad si son muchos pedidos
        event, nombre, apellido = datos_comanda
        
        deudas = False
        texto = texto.get()    
        cursor, database = conectar_db()
        
        ultimo_pedido = False

        if cursor and database:
            try:
                if texto != "Anular":
                    #si el pedido se despacho, significa que hay un total.
                    #si el texto no es despachar significa que es en camino.
                    if texto == "Despachar":
                        consulta = messagebox.askyesno(title="Caja", message=u"¿Es fiado?")
                        if consulta:
                            texto="Fiados"
                            deudas = True
                        else:
                            texto="Despachados"

                        consulta = f_consulta_pedidos(cursor, id_pedido, texto)
                        consulta = consulta.fetchone()
                        consulta = list(consulta)


                        #ESTADO 
                        consulta.append(texto)

                        if texto == "Fiados" and consulta[17]:
                            consulta[17] = 0
                            messagebox.showinfo(title="Aviso",
                                                message="Si el pedido es fiado, no se aplica descuento")
                        
                        cursor.execute("""INSERT INTO PEDIDOSDESPACHADOS(MENU, CANTIDADMENU, PRECIOMENU,
                                          GUARNICION, CANTIDADGUARNICION, PRECIOGUARNICION,
                                          BEBIDA, CANTIDADBEBIDA, PRECIOBEBIDA,
                                          POSTRE, CANTIDADPOSTRE, PRECIOPOSTRE,
                                          PROMOCION, CANTIDADPROMO, PRECIOPROMO,
                                          FECHA, CARGOENVIO, PORCENTAJE,
                                          TOTAL, idCLIENTE, ESTADO)
                                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""" , consulta)
                            
                        cursor.execute("DELETE FROM PEDIDO WHERE idPEDIDO=%d" % (id_pedido))
                            
                        #actualizamos el precio total que figura
                        p_actual = int(label_precio.cget('text'))
                        p_actual = p_actual - total
                        label_precio.config(text='%d' % p_actual)

                    if texto == "Preparado":
                        #como usamos la funcion bind, esta nos pasa el objeto que disparo el evento
                        #para acceder a sus propiedas y modificarlas usamos .widget
                        if boton_opcion:
                            boton_opcion.widget.config(relief=SUNKEN)

                    cursor.execute("UPDATE PEDIDO SET ESTADO='%s' WHERE idPEDIDO=%d" % (texto, id_pedido))
                            
                else:
                    consulta = messagebox.askyesno(title="Anular pedido", message=u"¿Desea realmente anular el pedido?")
                    if consulta:
                        #reseteamos el cargo de envio del cliente
                        id_cliente = cursor.execute("SELECT idCLIENTE FROM PEDIDO WHERE idPEDIDO='%d'" % id_pedido)
                        id_cliente = id_cliente.fetchone()

                        cursor.execute("UPDATE CLIENTE SET idCARGOENVIO=0 WHERE idCLIENTE='%d'" % id_cliente)
                        
                        cursor.execute("DELETE FROM PEDIDO WHERE idPEDIDO=%d" % (id_pedido))

                        messagebox.showinfo(title="Resultado", message="Pedido anulado")

                    else:
                        #presiono por error
                        return 0

                if texto != "Preparado":
                    if self.cantidad_widget > 1:
                        self.cantidad_widget = self.cantidad_widget - 1
                        event.widget.config(text=TEXTO_COMANDA % (nombre, apellido, self.cantidad_widget))
                        frame.destroy()
                        self.update()
                        canvas.config(scrollregion=canvas.bbox("all"))
                    else:
                        ultimo_pedido = True
                        #Por el momento no podemos eliminar el widget y rellenar ese espacio vacio
                        #asi que lo desabilitamos y le cambiamos el texto.
                        #texto_widget = frame_comanda.children['!label'].cget('text')
                    
                        frame_comanda.children['!label'].config(text="Procesado",
                                                                 fg="#646184",
                                                                 state=DISABLED,
                                                                 relief=SUNKEN)
                        self.frame_en_proceso.update_idletasks()
                        self.frame_en_proceso.update()
                        if texto != "Anular":
                            self.reset_envio(cursor, id_cliente)
                        ventana.destroy()
                        
                    if texto == "Despachados":
                        self.insertar_en_caja(total=total, cursor=cursor, pago_deudas=False,
                                              envios=cargo_envio if ultimo_pedido else None)

                #hacemos un commit cuando todo salio ok
                cursor.connection.commit()
            
            except db.Error:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            else:
                database.close()

def verificar_estado_delivery(self, id_cliente, ventana=None, frame_comanda=None):
        cursor, database = conectar_db()
        if cursor and database:
            try:
                consulta = cursor.execute("""SELECT pe.ESTADO FROM PEDIDO pe
                                             INNER JOIN CLIENTE c ON pe.idCLIENTE = c.idCLIENTE
                                             WHERE c.idCLIENTE='%d'""" % id_cliente)
                consulta = consulta.fetchall()

                for estado in consulta:
                    if estado[0] != "Preparado" and estado[0] != "Despachados" and estado[0] != "Fiados" and estado[0] != "En camino":
                        messagebox.showerror(title="Aviso",
                                             message="Todos los pedidos deben estar preparados para que el delivery los lleve")
                        return 0
            except db.Error:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            else:
                database.close()
                
                if self.cambiar_estado_preparados(id_cliente):
                    frame_comanda.children['!label'].config(text="Procesado",
                                                                 fg="#646184",
                                                                 state=DISABLED,
                                                                 relief=SUNKEN)
                    ventana.destroy()
    
    def cambiar_estado_preparados(self, id_cliente):
        cursor, database = conectar_db()
        if cursor and database:
            try:
                cursor.execute("""UPDATE PEDIDO SET ESTADO='%s'
                               WHERE idCLIENTE='%d' AND ESTADO='Preparado'""" % ('En camino', id_cliente))
                cursor.connection.commit()
            except db.Error:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
                return 0
            else:
                database.close()
                return True
