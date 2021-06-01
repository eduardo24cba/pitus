from archivos.funciones import conectar_db


def guardar_pedido(modificar_pedido, listbox_factura, lista_var, clases, lista_labels, lista_ccbox, botones, precio_total,
                   descuento, cargo_envio, b_descuento, b_envio, id_=None, nuevo_pedido=False):

        cursor, database = conectar_db()
        #fecha
        tiene_envio = False
        tiene_descuento = False
        descuento_all_pedidos = False
       
        insertar_envio = False
        insertar_descuento = False

        
        if obtener_fecha(fecha=True):
            fecha = obtener_fecha(fecha=True)

        #El estado siempre sera en proceso
        estado  = "En proceso"
        hora    = time.strftime("%I:%M:%S")

        #casos antes de guardar el producto
        #caso 1 no se selecciono ningun producto, y se oprimio el boton guardar

        if not listbox_factura.size():
            messagebox.showerror(title="Error", message=u"Debes seleccionar algún producto")
            return 0

            #seleccionamos todas las cantidades y los menus
            ids_menu, cantidades_menu = agregar_cantidad_and_ids(clases)

        #caso 2
        #se selecciono algun producto y no se selecciono ningun cliente

        if not self.buscar_cliente.id_cliente.get():
            messagebox.showinfo(title="Error", message=u"Debes seleccionar un cliente")
            return 0
        else:
            #si paso el caso 3 entendemos que se ha seleccionado un cliente
            #obtenemos su id y luego la pasamos a la tupla

            id_cliente = self.buscar_cliente.id_cliente.get()

        #caso 4, no se selecciono una opcion de envio
        if not self.opcion_entrega.get():
            messagebox.showinfo(title=u"Opción de entrega", message=u"Debes seleccionar una opción\nDelivery o Retira")
            return 0
        else:
            envio = verificar_envio(id_cliente)
            
            if envio and not self.opcion_entrega.get() in envio:
                messagebox.showinfo(title=u"Opción de entrega",
                message=u"El cliente ya ha realizado un/os pedido/s con la opción %s\n" % envio+
                         u"La opción de envío para este pedido debe ser igual\n"+
                         u"Si desea modificar la entrega debe ingresar a los pedidos "+
                         u"del cliente y cambiarla desde ahí." )
                return 0
          
            if self.opcion_entrega.get() == "Delivery":
                if verificar_cargo_envio(id_cliente):
                    tiene_envio = True

                #tiene envio y apreto quitar envio
                #tiene envio y selecciono quitar envio, esto se sabe porque
                #la variable envio se setea con los datos del cliente

                if tiene_envio and not cargo_envio.get():
                    consulta = messagebox.askyesno(title="Aviso",
                                                   message=AVISO_CARGOENVIO)
                    if not consulta:
                        return 0
                    else:
                        insertar_envio = True
                            
                else:
                    #no tiene envio y no selecciono cargo de envio
                    if not tiene_envio and not cargo_envio.get():
                        consulta = messagebox.askyesno(title="Envio",
                                                       message=u"No aplico ningún cargo de envío\n¿Desea aplicar?")
                        if consulta:return 0
                        else:pass

                    #selecciono envio pero no tenia con anterioridad
                    if not tiene_envio and cargo_envio.get():
                        insertar_envio = True
            else:
                if cargo_envio.get():
                    messagebox.showinfo(title=u"Cargo de envío",
                                        message=u"Si el pedido se retira en puerta no puede aplicarse cargo de envío")
                    return 0
        #--verificamos que tengo cargo de envio o descuento--#
        
        if verificar_descuento(id_cliente):
            tiene_descuento = True

        #tiene descuento y selecciono quitar descuento
        if tiene_descuento and not descuento.get():
            consulta = messagebox.askyesno(title="Aviso",
                                           message=AVISO_DESCUENTO)
            if not consulta:
                return 0
            else:
                insertar_descuento = True
                quitar_agregar_descuento(id_cliente, True)

        else:
            if descuento.get() and not tiene_descuento:
                #Ingreso un nuevo pedido y logro descuento
                #entonces debemos aplicar descuento a todos los pedidos
                #nos paso con un caso de un pedido ya listo para salir por el delivery
                
                descuento_all_pedidos = True
                insertar_descuento = True
                quitar_agregar_descuento(id_cliente, False)
    

        #caso 5, la guarnicion se cobra aparte o no
        #si es True, no se cobra, acompania.
        #----------corroborar que no de error esto------
        if self.bool_guarnicion.get():
            precio_guarnicion = 0
        else:
            precio_guarnicion = clases[1].dic_menu.get(
                 clases[1].var_menu.get())[0]

        #datos del pedido
        lista_datos =[ids_menu[0], cantidades_menu[0], clases[1].var_menu.get(),
                      cantidades_menu[1], precio_guarnicion, ids_menu[2], cantidades_menu[2],
                      ids_menu[3], cantidades_menu[3], ids_menu[4], cantidades_menu[4],
                      estado, descuento.get(), self.opcion_entrega.get(), fecha, hora, id_cliente]


        if cursor and database:
            try:
                if not modificar_pedido.get():
                    lista_datos = tuple(lista_datos)

                    cursor.execute("""INSERT INTO PEDIDO(idMENU, CANTIDADMENU,
                                      GUARNICION, CANTIDADGUARNICION, PRECIOGUARNICION,
                                      idBEBIDA, CANTIDADBEBIDA, idPOSTRE, CANTIDADPOSTRE,
                                      idPROMO, CANTIDADPROMO, ESTADO, idDESCUENTO, ENTREGA, FECHA,
                                      HORA, idCLIENTE)
                                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", lista_datos)
                else:
                    #se agrega la id del pedido, entendemos que tiene
                    lista_datos.append(id_)
                    lista_datos = tuple(lista_datos)

                    cursor.execute("""UPDATE PEDIDO SET idMENU='%d', CANTIDADMENU='%d',
                                      GUARNICION='%s', CANTIDADGUARNICION='%d', PRECIOGUARNICION='%d',
                                      idBEBIDA='%d', CANTIDADBEBIDA='%d', idPOSTRE='%d', CANTIDADPOSTRE='%d',
                                      idPROMO='%d', CANTIDADPROMO='%d', ESTADO='%s', idDESCUENTO='%d', ENTREGA='%s',
                                      FECHA='%s', HORA='%s', idCLIENTE='%d'
                                      WHERE idPEDIDO='%d'""" % lista_datos)
                    
                #si el pedido llego hasta esta instancia se entiende que existe un cliente
                if insertar_envio:
                    cursor.execute("UPDATE CLIENTE SET idCARGOENVIO='%d' WHERE idCLIENTE='%d'" % (cargo_envio.get(), id_cliente))

                #aplicamos descuento a todos los pedidos ya realizados por el cliente
                #si hubiese mas de 1...
                if descuento_all_pedidos:
                    descuento_multiples_pedidos(id_cliente, cursor)
                
                cursor.connection.commit()

                messagebox.showinfo(title="Resultado", message="Pedido guardado con exito")
                
                default_ccbox(lista_ccbox)
                clases[4].borrar_promo()

                if nuevo_pedido:
                    #Generamos un nuevo pedido del mismo cliente
                    #la lista de labels contiene los datos del cliente
                    #que son los ultimos 2.       
                    default_labels(lista_labels[:-2])
                    desactivar_botones(botones)#no desactivamos el boton nuevo pedido
                    default_variables(lista_var[:-2])#no reseteamos el cargo envio y descuento del cliente
                    
                else:
                    #si no existe un nuevo pedido, no existe modificar
                    self.buscar_cliente.id_cliente.set(0)
                    #se setea aca, y no se adjunta con las demas variables
                    #dado que paso que unas veces python lo setea con "0" o directamente no lo hace
                    #en la funcion default_variables, y tira error.
                    #es raro que unas veces funcione y otras no.
                    self.opcion_entrega.set("")
                    #activamos labels, botones.
                    default_labels(lista_labels)
                    default_variables(lista_var)
                    activar_botones(botones)
                    b_descuento.config(text=DESCUENTO % 0 )
                    b_envio.config(text=ENVIO % 0)

                if self.datos_modificar_pedido:
                    #se borran los datos para que no se siga rellenando
                    #cada vez que cambiemos de pestanias
                    #se habilitan las pestanias
                    self.datos_modificar_pedido.clear()
                    modificar_pedido.set(False)
                    self.notebook.tab(1, state="normal")
                    self.notebook.tab(2, state="normal")

                #colocamos el precio total aca, porque abajo del mensaje guardado con exito
                #no funcionaba... 
                precio_total.config(text="Precio total: $0")
    
            except db.Error:
                messagebox.showerror(title="Error", message="No se ha podido guardar el pedido %s" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror(title="Error", message="No se ha podido guardar el pedido.\n%s" % traceback.format_exc())
                return 0
            except:
                messagebox.showerror(title="Error", message="No se ha podido guardar el pedido\nError 4012.")
                return 0
            else:
                database.close()
        else:
            messagebox.showerror(title="Error", message="No se ha podido establecer la conexion con la base de datos")
            return 0
