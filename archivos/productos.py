import tkinter as tk
import traceback

from archivos.funciones import rellenar_diccionario, crear_ventana, centrar, conectar_db, desactivar_activar_tabs
from archivos.multibox import MultiListbox
from archivos.caracter import es_num
from tkinter import ttk
from tkinter import messagebox

fuente_responsive = ('Tahoma', 12, 'bold')

class Producto:

    #diccionarios que almacenan la id del producto seleccionado
    dic_menu = {}
    dic_guarnicion = {}
    dic_bebida = {}
    dic_postre = {}

    def __init__(self, parent):

        self.parent = parent
        self.notebook = None

        self.factura = None
        self.var_precio_total = None
        self.label_precio_total = None
        self.var_error = tk.IntVar(parent)
        self.producto_seleccionado = tk.IntVar(parent)
        

        self.var_error.set(0)
        self.producto_seleccionado.set(0)

    def ventana_producto(self, opcion):

        # las opciones son: menu, guarnicion, postre, bebida o cliente
        opcion = opcion.upper()

        ventana = crear_ventana(self.parent, resizable=True, bg="#FF6961")

        #Se crea primero la listbox asi podemos despues de consultar la base de datos rellenarla

        lista_productos = MultiListbox(ventana,
                                    (('Producto', 40), ('Precio', 8)),
                                    alto_ancho=(300, 500), alineacion="nw", selectbackground="red")

        #no hay tabla, hay que pasar el diccionario a la variable buscar trace.

        if opcion   == "MENU": 
            rellenar_diccionario(self.dic_menu, lista_productos=lista_productos, opcion=opcion,)
            dic_producto = self.dic_menu
        
        elif opcion == "GUARNICION":
            rellenar_diccionario(self.dic_guarnicion, lista_productos=lista_productos, opcion=opcion)
            dic_producto = self.dic_guarnicion

        elif opcion == "BEBIDA":
            rellenar_diccionario(self.dic_bebida, lista_productos=lista_productos, opcion=opcion)
            dic_producto = self.dic_bebida

        else:
            #opcion == "POSTRE"
            rellenar_diccionario(self.dic_postre,  lista_productos=lista_productos, opcion=opcion)
            dic_producto = self.dic_postre


        pad_x = 2
        pad_y = 2

        var_buscar = tk.StringVar(ventana)
        var_seleccion = tk.StringVar(ventana)
        var_cantidad = tk.IntVar(ventana, value=0)

        # se setea dado que cuando ingresamos de nuevo
        # se quedan guardados los datos
        var_buscar.set("")
        var_seleccion.set("")

        label_b = tk.Label(ventana, font=fuente_responsive,
                        text="Buescar producto")

        buscar = tk.Entry(ventana, font=fuente_responsive,
                        width=25, textvariable=var_buscar)

        label_c = tk.Label(ventana, font=fuente_responsive, text="Cantidad")
        
        cantidad = tk.Spinbox(ventana, font=fuente_responsive,
                            width=4, to=1000, textvariable=var_cantidad)
        
        buscar.focus()

        seleccionar = tk.Button(ventana, font=fuente_responsive, text="Seleccionar",
                                command=lambda: self.seleccion_producto(lista_productos, var_seleccion, cantidad, ventana))

        var_buscar.trace('w', (lambda var, name, type_: self.buscar_en_lista(
                               var_buscar, var, name, type_,
                               lista_productos, list(sorted(dic_producto.keys()))
                               )
                            )
                        )

        label_b.grid(row=0, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
        buscar.grid(row=0, column=1, sticky="nsew", padx=pad_x, pady=pad_y)
        label_c.grid(row=0, column=2, sticky="nsew", padx=pad_x, pady=pad_y)
        cantidad.grid(row=0, column=3, sticky="nsew", padx=pad_x, pady=pad_y)

        lista_productos.grid(row=2, column=0, columnspan=4,
                            sticky="nsew", padx=pad_x, pady=pad_y)

        seleccionar.grid(row=3, column=3, sticky="nsew", padx=pad_x, pady=pad_y)

        #asignamos el return a los widgets para que presione enter
        #y pueda seleccionar el producto, otra alternativa

        cantidad.bind(       "<Return>", lambda e: self.seleccion_producto(lista_productos, var_seleccion, cantidad, ventana, e))
        buscar.bind(         "<Return>", lambda e: self.seleccion_producto(lista_productos, var_seleccion, cantidad, ventana, e))
        lista_productos.bind("<Return>", lambda e: self.seleccion_producto(lista_productos, var_seleccion, cantidad, ventana, e))

        centrar(ventana)

    def seleccion_producto(self, lista_productos, var_seleccion, cantidad, ventana, event=None):
        """
        ingresamos los elementos en la listbox factura
        """

        # primero sacamos todos los espacios
        cantidad = "".join(cantidad.get().split())

        if not es_num(cantidad):
            messagebox.showerror(
                "Error", "Debes ingresar números en el campo cantidad")
            return 0

        # la cantidad es un numero
        cantidad = int(cantidad)

        if lista_productos.curselection() and cantidad:

            producto, precio_unit = lista_productos.get(
                lista_productos.curselection())

            monto = cantidad * int(precio_unit)

            self.factura.insert(tk.END, (producto, cantidad,
                                    precio_unit, monto))

            total_anterior = self.var_precio_total.get()

            self.var_precio_total.set(total_anterior + monto)

            self.label_precio_total.config(text="Total: %d" %  self.var_precio_total.get())

            desactivar_activar_tabs(self.notebook, desactivar=True)

            self.producto_seleccionado.set(1)

            ventana.destroy()
        else:
            messagebox.showerror(
                "Error", "Debes seleccionar un producto y una cantidad")
            return 0


    def ventana_agregar_producto(self, datos=None):
        #agregar o modificar
        
        ancho = 30

        fuente_wid = ('Tahoma', 12, 'bold')

        ventana = crear_ventana(self.parent, resizable=True)

        var_tipo_producto = tk.StringVar(self.parent)

        var_precio = tk.IntVar(self.parent)
        var_precio.set(0)

        label_menu_ = tk.Label(ventana, font=fuente_wid,
                            text=u"Producto")

        label_precio_ = tk.Label(ventana, font=fuente_wid, text=u"Precio")

        label_text = tk.Label(ventana, font=fuente_wid, justify=tk.LEFT, 
                            text=u"Descripción del producto:\n- Si es un menú\ningresa los ingredientes\n-"+
                            "Si es una bebida\ningresa el tipo de bebida:\n2 litros, 1 Litro, etc")

        label_tipo = tk.Label(ventana, font=fuente_wid, text="Tipo de producto")

        menu   = tk.Entry(ventana, font=fuente_wid, width=ancho)
        precio = tk.Entry(ventana, font=fuente_wid, width=ancho, textvariable=var_precio)
        texto  = tk.Text( ventana, font=fuente_wid, width=ancho, height=10, wrap=tk.WORD)
        
        tipo_producto = ttk.Combobox(ventana, font=fuente_wid, width=ancho, state="readonly", textvariable=var_tipo_producto)
        
        tipo_producto["values"] = ["MENU", "GUARNICION", "BEBIDA", "POSTRE", "PROMOCION"]

        menu.focus()

        if datos:
            #modificamos el producto
            pass

        aceptar = tk.Button(ventana, font=fuente_wid, text="Aceptar",
                            command=lambda:self.guardar_producto((menu, var_precio, texto, var_tipo_producto), ventana))

        #label_text = tk.Label(ventana, font=fuente_wid)

        label_menu_.grid(row=0, column=0, padx=2, pady=6, sticky="nsew")
        
        label_precio_.grid(row=2, column=0, padx=2, pady=6, sticky="nsew")

        menu.grid(row=0, column=1, padx=2, pady=6, sticky="nsew")
        
        precio.grid(row=2, column=1, padx=2, pady=6, sticky="nsew")

        label_text.grid(row=3, column=0, padx=2, pady=6, sticky="nsew")

        texto.grid(row=3, column=1, padx=2, pady=6, sticky="nsew")

        label_tipo.grid(row=4, column=0)

        tipo_producto.grid(row=4, column=1)

        aceptar.grid(row=5, column=1)

        centrar(ventana)

    def guardar_producto(self, datos, ventana):
        
        labels = ("Producto", "Precio", "Descripción", "Tipo producto")

        datos_productos = []

        try:
            #si no es número el campo precio, entonces informamos el error
            datos[1].get()
        except tk.TclError:
            messagebox.showerror("Error", "El campo %s acepta solo números" % labels[1])
            return 0

        #segunda verificacion
        for dato in range(len(datos)):
            if labels[dato] != "Descripción":
                if not datos[dato].get():
                    messagebox.showerror("Error", "Debes rellenar el campo %s" % labels[dato])
                    return 0
                else:
                    datos_productos.append(datos[dato].get())
            else:
                if not datos[dato].get("1.0", "end-1c"):
                    messagebox.showerror("Error", "Debes rellenar el campo %s" % labels[dato])
                    return 0
                else:
                    datos_productos.append(datos[dato].get("1.0", "end-1c").capitalize())

        consulta = messagebox.askyesno("Consulta", "Se va a guardar un nuevo producto ¿Están todos los datos correctos?")
        
        if not consulta:
            #oprimio que no
            return 0

        # oprimio que si

        #todos validados ok.

        #producto, precio, descripcion, tipo_producto = [dato for dato in range(len]

        #datos[0].get(), datos[1].get(), datos[2].get("1.0", "end-1c"), datos[3].get().capitalize()
        
        for dato in range(len(datos_productos)):

            if dato != 1: #la posicion 1 es el precio, no debe ser string
                datos_productos[dato] = " ".join(datos_productos[dato].split())

            if dato != 1 and dato != 3:
                datos_productos[dato] = datos_productos[dato].capitalize()

        datos_productos = tuple(datos_productos)
        
        cursor, database = conectar_db()

        if cursor and database:
            try:
                cursor.execute("INSERT INTO PRODUCTO(PRODUCTO, PRECIO, DESCRIPCION, TIPOPRODUCTO) VALUES('%s','%d','%s','%s')"
                                    % datos_productos)
                
                id = cursor.lastrowid

                tipo_producto = datos_productos[3].upper()

                #agregamos el nuevo producto al diccionario
                if tipo_producto   == "MENU": rellenar_diccionario(self.dic_menu, item=(datos_productos[0], datos_productos[1], id), opcion="MENU", nuevo_item=True, var=self.var_error)
                elif tipo_producto == "GUARNICION": rellenar_diccionario(self.dic_guarnicion, item=(datos_productos[0], datos_productos[1], id), opcion="GUARNICION", nuevo_item=True, var=self.var_error)
                elif tipo_producto == "BEBIDA": rellenar_diccionario(self.dic_bebida, item=(datos_productos[0], datos_productos[1], id), opcion="BEBIDA", nuevo_item=True, var=self.var_error)
                elif tipo_producto == "POSTRE": rellenar_diccionario(self.dic_postre, item=(datos_productos[0], datos_productos[1], id), opcion="POSTRE", nuevo_item=True, var=self.var_error)

                #si el producto ya existe en el diccionario, se asigna 1 a la variable dic
                if self.var_error.get():
                    return 0
                    

            except Exception:
                messagebox.showerror("Error", "%s" % traceback.format_exc())
                return 0
            
            else:
                #todo salio bien
                cursor.connection.commit()
                messagebox.showinfo(messagebox.INFO, "Producto agregado con éxito")
                ventana.destroy()

            finally:
                database.close()
        
        
    def buscar_en_lista(self, var_buscar, name, var, type_, lista_productos, menu):
        # se borran los items que esten seleccionados
        # se selecciona el item que coincida
        # el scroll se mueve gracias a see()
        # se busca el producto a medida que va tecleando, sino coincide no se selecciona ninguno

        try:
            value = var_buscar.get().capitalize()
        except Exception:
            messagebox.showerror(title=messagebox.ERROR,
                                message="Error funcion buscar en lista %s" % traceback.format_exc())
            return 0

        if value:

            try:

                index = 0
                for x in range(0, len(menu)):

                    # menu[x][:len(value)] es: la primera x va iterando sobre la lista y nos trae las palabras
                    # len(value) va avanzando a medida que escribimos. Ej.
                    # Escribimos C -> busca todas las palabras con C. Ca -> Va achicando la busqueda
                    if value == str(menu[x][:len(value)]):
                        index = x
                        lista_productos.selection_clear(0, tk.END)
                        lista_productos.activate(index)
                        lista_productos.see(index)

                        break

                    else:

                        # si sigue escribiendo y no coincide
                        # se borra la seleccion que exista
                        lista_productos.selection_clear(0, tk.END)

            except Exception:
                
                # tenemos un error, la referencia a esta clase se mantiene
                # no se elimina cuando el cliente ha presionado buscar cliente
                # y luego, ha cambiado de pestania y ha vuelto a presionar
                # buscar cliente... si cierra la ventana y vuelve a presionar
                # el error desaparece. Por ahora, la forma de que no tire error
                # es capturar la exepcion y dejarla pasar
                messagebox.showerror(messagebox.ERROR, "Error funcion buscar_en_lista clase productos %s" % traceback.format_exc())
        else:
            # no hay valores ingresados en el entry, se borraron
            try:
                lista_productos.selection_clear(0, END)

            except:
                pass