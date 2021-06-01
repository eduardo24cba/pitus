    def pedidos_despachados(self, boton):
        if comprobar_si_hay_pedido(self.datos_modificar_pedido):
            messagebox.showwarning(title="Aviso", message=AVISO_DATOS_PEDIDO)
            return 0
        
        self.comprobar(self.notebook)
        self.marcar_activo(boton)
        self.frame_ventanas = self.crear_frame()
        alto, ancho = widget_responsive(self, 50, 180)
        self.frame_ventanas.config(bg="#adabae", width=ancho, height=alto)
        alto_listbox = alto /5
        alto_listbox = int(alto_listbox)

        alto_widget = 1
        ancho_widget = 3
        ancho_wid_bottom = alto_widget + 8
        ancho_fuente = 7
        pad_x = 1

        fuente_responsive = ('Tahoma', ancho_fuente,'bold')

        tamanio_fuente = round(alto_listbox / 20) - 1

        cursor,database = conectar_db()
        #creamos una lista con los menus
        consulta = cursor.execute("SELECT MENU FROM MENU WHERE MENU != '-' ORDER BY MENU ASC ")
        consulta = consulta.fetchall()
        menu = [item[0] for item in consulta]

        #variables para el control de las funciones
        var_inicio = StringVar(self.frame_ventanas, name="inicio")
        var_fin    = StringVar(self.frame_ventanas, name="fin")
        var_menu   = StringVar(self.frame_ventanas, name="menu")
        var_opcion = StringVar(self.frame_ventanas, name="opcion")

        mes_elegido = StringVar(self.frame_ventanas)
        anio_elegido= StringVar(self.frame_ventanas)
        dia_elegido = StringVar(self.frame_ventanas)

        #dependiendo el estado, el calendario mostrara
        #los botones siguiente y anterior
        var_estado = StringVar(self.frame_ventanas)
        var_estado.set("normal")

        opciones = ["Todos", "Fiados", "Pagados"]
        

        #definimos los widgets

        label_despachados = Label(self.frame_ventanas, font=fuente_wid, bg="#e3c8c8", relief=GROOVE)
        label_fiados      = Label(self.frame_ventanas, font=fuente_wid, bg="#bedabe", relief=GROOVE)        

        boton_seleccion= Button(self.frame_ventanas,  height=alto_widget, font=fuente_responsive,  text=u"Selección día")
        label_info = Label(self.frame_ventanas, text=INFO_SELECCION)
        
        label_menu   = Label(self.frame_ventanas,  width=ancho_widget, height=alto_widget, font=fuente_responsive, text=u"Menú")
        boton_desde  = Button(self.frame_ventanas, width=ancho_widget, height=alto_widget, font=fuente_responsive, text="Desde")
        boton_hasta  = Button(self.frame_ventanas, width=ancho_widget, height=alto_widget, font=fuente_responsive, text="Hasta", state='disabled')
        
        boton_aceptar= Button(self.frame_ventanas, width=ancho_widget, height=alto_widget, font=fuente_responsive, text="Aceptar")
        boton_limpiar= Button(self.frame_ventanas, width=ancho_widget, height=alto_widget, font=fuente_responsive, text="Limpiar")

        lista_desplegable = ttk.Combobox(self.frame_ventanas, state="readonly",
                                                  width=ancho_widget, height=alto_widget, font=fuente_responsive, 
                                                  textvariable=var_menu)
        label_opcion = Label(self.frame_ventanas, width=12, height=alto_widget, font=fuente_responsive,  text="Opcion")

        lista_opciones = ttk.Combobox(self.frame_ventanas, state="readonly",
                                                  width=ancho_widget, height=alto_widget, font=fuente_responsive, 
                                                  textvariable=var_opcion)
        
        label_guia = Label(self.frame_ventanas, text=ESTADISTICA, justify=LEFT)
        
        lista_desplegable["values"] = menu
        lista_opciones["values"] = opciones

        lista_pedidos_despachados = MultiListbox(self.frame_ventanas,
                            ((u'Menú', 30), ('Cantidad', 8), ('Precio unitario', 8),
                             (u'Guarnición', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Bebida', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Postre', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Promocion', 50),('Cantidad', 8),('Precio unitario', 8),
                             ('Fecha', 10), ('Hora de despacho',8), 
                             ('Descuento',8), ('Total',8)),
                             expand_total=True,
                            alto_ancho=(alto_listbox, ancho), alto=tamanio_fuente, bg='white')

        lista_pedidos_fiados = MultiListbox(self.frame_ventanas,
                            ((u'Menú', 30), ('Cantidad', 8), ('Precio unitario', 8),
                             (u'Guarnición', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Bebida', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Postre', 20),('Cantidad', 8),('Precio unitario', 8),
                             ('Promocion', 50),('Cantidad', 8),('Precio unitario', 8),
                             ('Fecha', 10), ('Hora de despacho',8),
                             ('Descuento',8), ('Total',8)),
                             expand_total=True,
                            alto_ancho=(alto_listbox, ancho), alto=tamanio_fuente, bg='white')

        #la clase que nos proporciona los graficos
        pedidos_vendidos = PedidosVendidos(self)
        
        #configuramos las opciones para cada boton
        boton_seleccion.configure(
            command=lambda:pedidos_vendidos.pedidos_dia(self, lista_pedidos_despachados,
                                                        lista_pedidos_fiados,
                                                        label_despachados,
                                                        label_fiados,
                                                        cursor, database))
        boton_desde.configure(
            command=lambda:pedidos_vendidos.crear_calendario(self, var_inicio,
                                                        boton_desde,
                                                        boton_hasta,
                                                        mes_elegido,
                                                        anio_elegido,
                                                        dia_elegido,
                                                        var_estado))
        boton_hasta.configure(
            command=lambda:pedidos_vendidos.crear_calendario(self, var_fin,
                                                        boton_desde,
                                                        boton_hasta,
                                                        mes_elegido,
                                                        anio_elegido,
                                                        dia_elegido,
                                                        var_estado))

        boton_aceptar.configure(
            command=lambda:pedidos_vendidos.mostrar(self, var_inicio,
                                                        var_fin,    
                                                        var_menu,
                                                        var_opcion,
                                                        mes_elegido))
        boton_limpiar.configure(
            command=lambda:reset_grafica(var_inicio,
                                         var_fin,
                                         lista_desplegable,
                                         lista_opciones,
                                         var_menu,
                                         var_opcion,
                                         boton_desde,
                                         boton_hasta,
                                         mes_elegido,
                                         anio_elegido,
                                         var_estado))
        if obtener_fecha(fecha=True):
            fecha = obtener_fecha(fecha=True)
        #pasamos las listas, labels a la funcion para que nos las rellene
        #existan datos o no

        database.close()
        
        pedidos_vendidos.mostar_pedidos_dia(lista_pedidos_despachados,
                                            lista_pedidos_fiados,
                                            label_despachados,
                                            label_fiados, fecha)

        #label que se ubica encima de las listbox's
        label_despachados.grid(row=4, column=0, sticky="nsew", columnspan=8)
        label_fiados.grid(row=6, column=0, sticky="nsew", columnspan=8)

        #listbox's
        lista_pedidos_despachados.grid(row=5, column=0, columnspan=16, pady=5)
        lista_pedidos_fiados.grid(     row=7, column=0, columnspan=16, pady=5)
        
        x=2
        y=3

        #label del menu
        label_menu.grid(row=8, column=0, sticky="nsew", padx=x, pady=y, columnspan=2)
        lista_desplegable.grid(row=9, column=0, sticky="nsew",
                               padx=x, pady=y, columnspan=2)
        
        #
        label_opcion.grid(  row=8, column=2, sticky="nsew", padx=x, pady=y, columnspan=2)
        lista_opciones.grid(row=9, column=2, sticky="nsew", padx=x, pady=y, columnspan=2)
        
        #
        boton_desde.grid(   row=10, column=0, sticky="nsew", padx=x, pady=y)
        boton_hasta.grid(   row=10, column=1, sticky="nsew", padx=x, pady=y)
        boton_limpiar.grid( row=11, column=0, sticky="nsew", padx=x, pady=y)
        boton_aceptar.grid( row=11, column=1, sticky="nsew", padx=x, pady=y)
        label_guia.grid(    row=12, column=0, sticky="nsew", padx=x, pady=y, columnspan=6)

        label_info.grid(     row=8, column=8, padx=x, pady=y, sticky="nsew")
        boton_seleccion.grid(row=9, column=8, padx=x, pady=y, sticky="nw")   
