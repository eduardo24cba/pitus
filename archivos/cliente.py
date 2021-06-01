from tkinter import ttk
from tkinter import messagebox

from archivos.funciones import crear_ventana, validar_cliente, conectar_db, centrar, desactivar_activar_tabs
from archivos.entrega import verificar_cargo_envio
from archivos.multibox import MultiListbox
from archivos.constantes import ENVIO, DESCUENTO, NOMBRE_CLIENTE, PRECIO_TOTAL

import sqlite3 as db
import tkinter as tk
import traceback

ANCHO = 400
ALTO = 500


class Cliente:
    def __init__(self, parent, ):

        self.master = parent
        self.notebook = None
        
        self.label_cliente = None
        self.lista = None
        self.fuente = None
        self.id_cliente = tk.IntVar(parent, name="cliente")

        self.widgets = []

        self.var_buscar = None
        self.var_buscar = tk.StringVar(self.master, name="buscar")
        self.lista_clientes = None

        # afectamos envio o descuento cuando elegimos un cliente
        self.label_envio = None
        self.var_envio = None
        self.precio_actual = None
        self.label_precio_total = None
        self.total_envio = None

        self.costo_envio = 0

    def buscar_cliente(self):

        #si hay cliente mostraremos un alerta que eliminara al cliente
        if self.id_cliente.get():
            consulta = messagebox.askyesno("Consulta cliente", "Ya hay un cliente seleccionado.\n"+
                                          "¿Desea elegir uno nuevo?\n"+
                                          "esto eliminara al cliente actual.")
            if consulta:
                self.label_cliente.config(text=NOMBRE_CLIENTE)
                self.id_cliente.set(0)

                #si hay un cargo de envio aplicado debemos quitarlo
                if self.var_envio.get():

                    self.var_envio.set(0)

                    precio_actual = self.precio_actual.get() - self.costo_envio
            
                    self.precio_actual.set(precio_actual)

                    self.label_precio_total.config(text=PRECIO_TOTAL % precio_actual)

                    self.costo_envio = 0

                    self.total_envio.set(self.costo_envio)

                    self.label_envio.config(text=ENVIO % self.costo_envio)

            else:
                #no presiono cambiar entonces no le dejamos elegir otro cliente
                return 0


        if not self.lista:
            messagebox.showerror("Error", "No existen clientes, por favor agrega algunos para continuar.")
            return 0
        
        ventana = crear_ventana(self.master, resizable=True)

        # se setea dado que cuando ingresamos de nuevo
        # se quedan guardados los datos
        self.var_buscar.set("")

        label = tk.Label(ventana, font=self.fuente, text="Lote")
        buscar = tk.Entry(ventana, font=self.fuente, textvariable=self.var_buscar)
        buscar.focus()

        #asignamos el evento que al presionar enter seleccione el cliente
        buscar.bind("<Return>", lambda event, opcion="Seleccionar": self.verificar(opcion, ventana, event) )

        self.lista_clientes = MultiListbox(ventana,
                                           ((u'Numeración/Lote', 20), ('Calle/Manzana', 20),
                                            ('Telefono', 15), ('Barrio', 40)),
                                           expand_total=True, alto_ancho=(200, 200), alineacion="nw")

        seleccionar = tk.Button(ventana, font=self.fuente, text="Seleccionar",
                             command=lambda opcion="Seleccionar": self.verificar(opcion, ventana))
        
        modificar = tk.Button(ventana, font=self.fuente, text="Modificar",
                           command=lambda opcion="Modificar": self.verificar(opcion, ventana))

        for cliente in self.lista:
            self.lista_clientes.insert(
                tk.END, (cliente[0], cliente[1], cliente[2], cliente[3]))

        # trace pasa como primeros 2 argumentos 'w' y el nombre del la variable
        self.var_buscar.trace(
            'w', (lambda var, name, type_: self.buscar_en_lista(var, name, type_)))

        label.grid(row=0, column=0, sticky="nsew")
        buscar.grid(row=0, column=1, sticky="nsew")
        seleccionar.grid(row=0, column=2, sticky="nsew")
        modificar.grid(row=0, column=3, sticky="nsew")

        self.lista_clientes.grid(
            row=1, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        self.widgets.append(label)
        self.widgets.append(buscar)
        self.widgets.append(seleccionar)
        self.widgets.append(self.lista_clientes)
        
        centrar(ventana)

    def buscar_en_lista(self, name, var, type_):
        # se borran los items que esten seleccionados
        # se selecciona el item que coincida
        # el scroll se mueve gracias a see()
        # se busca por apellido dado que nombres son muchos
        # seria dificil encontrar al cliente solo por el nombre
        try:
            value = self.var_buscar.get().capitalize()
        except Exception as e:
            messagebox.showerror(title=("Error %s" % e),
                                 message="Error funcion buscar en lista")
            return 0

        if value:

            try:

                index = 0
                for x in range(0, len(self.lista)):

                    # si el valor coincide a medida que va escribiendo con lo que hay en la lista
                    # entonces rellenamos lo marcamos en la lista
                    if value == str(self.lista[x][0]):
                        index = x
                        self.lista_clientes.selection_clear(0, tk.END)
                        self.lista_clientes.activate(index)
                        self.lista_clientes.see(index)

                        break
                    else:
                        # si sigue escribiendo y no coincide
                        # se borra la seleccion que exista
                        self.lista_clientes.selection_clear(0, tk.END)
            except Exception as e:
                # tenemos un error, la referencia a esta clase se mantiene
                # no se elimina cuando el cliente ha presionado buscar cliente
                # y luego, ha cambiado de pestania y ha vuelto a presionar
                # buscar cliente... si cierra la ventana y vuelve a presionar
                # el error desaparece. Por ahora, la forma de que no tire error
                # es capturar la exepcion y dejarla pasar
                pass
        else:
            # no hay valores ingresados en el entry, se borraron
            try:
                self.lista_clientes.selection_clear(0, tk.END)

            except:
                pass

    def crear_cliente(self, main_ventana, desde_fuera=False, cliente=None, id_cliente=None, id_lista=None):

        # si creamos un cliente, tenemos dos opciones
        # una es ingresar desde la ventana pedidos
        # la otra es en la ventana clientes
        # preguntamos para saber a que se asocia la ventana

        if not desde_fuera:
            nueva_ventana = crear_ventana(main_ventana, resizable=True)
            nueva_ventana.wm_protocol('WM_DELETE_WINDOW',
                                      lambda ventana=nueva_ventana: self.destruir(ventana=nueva_ventana, principal=main_ventana))
        else:
            nueva_ventana = crear_ventana(main_ventana, resizable=True)

        label_nombres   = tk.Label(nueva_ventana, font=self.fuente, text=u"Numeración/Lote")
        
        label_apellidos = tk.Label(nueva_ventana, font=self.fuente, text="Calle/Manzana")
        
        label_telefono  = tk.Label(nueva_ventana, font=self.fuente, text=u"Teléfono")
        
        label_direccion = tk.Label(nueva_ventana, font=self.fuente, text="Barrio")

        nombres   = tk.Entry(nueva_ventana, font=self.fuente, width=30)
        apellidos = tk.Entry(nueva_ventana, font=self.fuente, width=30)
        telefono  = tk.Entry(nueva_ventana, font=self.fuente, width=30)
        direccion = tk.Text( nueva_ventana, font=self.fuente, width=30, height=4, wrap=tk.WORD)

        nombres.focus()

        boton_aceptar = tk.Button(nueva_ventana, text="Aceptar", font=self.fuente)

        # si existe un cliente, entonces modificamos datos
        if cliente:
            nombres.insert(tk.END, cliente[0])
            apellidos.insert(tk.END, cliente[1])
            telefono.insert(tk.END, cliente[2])
            direccion.insert('1.0', cliente[3])
            boton_aceptar.configure(command=lambda ventana=nueva_ventana,
                                    lista_datos=(nombres, apellidos, telefono, direccion):
                                    self.guardar_cliente(datos=lista_datos, ventana=ventana,
                                                         cliente=id_cliente, id_lista=id_lista,
                                                         ventana_principal=main_ventana))
        else:
            boton_aceptar.configure(command=lambda ventana=nueva_ventana,
                                    lista_datos=(nombres, apellidos, telefono, direccion):
                                    self.guardar_cliente(datos=lista_datos, ventana=ventana, ventana_principal=main_ventana))

        label_nombres.grid(  row=1, column=0, padx=5, pady=5)
        label_apellidos.grid(row=2, column=0, padx=5, pady=5)
        label_telefono.grid( row=3, column=0, padx=5, pady=5)
        label_direccion.grid(row=4, column=0, padx=5, pady=5)

        nombres.grid(  row=1, column=1, padx=5, pady=5)
        apellidos.grid(row=2, column=1, padx=5, pady=5)
        telefono.grid( row=3, column=1, padx=5, pady=5)
        direccion.grid(row=4, column=1, padx=5, pady=5, ipady=10)

        boton_aceptar.grid(row=5, column=1, padx=5, pady=5)
        centrar(nueva_ventana)

    def guardar_cliente(self, datos, ventana, ventana_principal, cliente=None, id_lista=None):
        # cliente es igual a la id_cliente
        # id_lista nos ayudara a actualizar los nuevos valores en la lista
        ultima_id = None

        # la id que se agregara a la lista
        id_cliente = None

        # los datos no son validos, se sale de la funcion, si son validos
        # se almacenaran.
        for x in datos[:3]:
            if not x.get():
                messagebox.showerror(title="Error",
                                     message="Debes rellenar todos los campos")
                return 0

        if not datos[3].get("1.0", "end-1c"):
            messagebox.showerror(title="Error",
                                 message="Debes rellenar todos los campos")
            return 0

        if not validar_cliente(datos):
            return 0

        lote, manzana, telefono, barrio = validar_cliente(datos)

        # insertamos cliente, obtenemos su ultimo id.
        # caputarmos los posibles errores y los mostramos.
        
        cursor, database = conectar_db()

        if cursor and database:
            try:
                if not cliente:
                    cursor.execute("""INSERT INTO CLIENTE(NUMERACIONOLOTE, CALLEOMANZANA, TELEFONO,BARRIO) VALUES('%s','%s','%d','%s')""" %
                                   (lote, manzana, telefono, barrio))
                    id_cliente = cursor.lastrowid
                else:
                    cursor.execute("""UPDATE CLIENTE SET NUMERACIONOLOTE='%s', CALLEOMANZANA='%s', TELEFONO='%d', BARRIO='%s' WHERE idCLIENTE='%d'""" %
                                   (lote, manzana, telefono, barrio, cliente))
                    id_cliente = cliente

                datos = lote, manzana, telefono, barrio, id_cliente
                # si el cliente se actualiza, hay cliente, por lo que se debe
                # marcar en la lista, para indicar ese cliente
                # de lo contrario se inserta con append
                # y se lo marca en la pestania pedidos

                if cliente:
                    self.lista[id_lista] = datos
                    self.actualizar_lista(index=id_lista)
                else:
                    self.lista.append(datos)
                    self.lista = sorted(self.lista)
                    self.setear_cliente(datos[:4])
                    self.id_cliente.set(id_cliente)

                if not cliente:
                    self.destruir(ventana=ventana, opcion=True)
                else:
                    self.destruir(ventana=ventana, principal=ventana_principal)

            except db.IntegrityError:
                messagebox.showerror(
                    title="Error", message="Ya existe un cliente con ese Lote y Manzana")
                return 0

            except db.Error as e:
                messagebox.showerror(
                    title="Error", message="No se ha podido guardar el cliente %s \nfuncion guardar_cliente" % e)
                return 0

            except Exception:
                messagebox.showerror(
                    title="Error", message="No se ha podido guardar el cliente.\n%s \nfuncion guardar_cliente" % traceback.format_exc())
                return 0

            else:
                # si no ocurrio ningun error, guardamos al cliente
                cursor.connection.commit()
                messagebox.showinfo(messagebox.INFO, "Cliente guardado con éxito")

            finally:
                database.close()

    def verificar(self, opcion, ventana, event=None):
        
        if self.lista_clientes.curselection():
            index = self.lista_clientes.curselection()
            persona = self.lista_clientes.get(index)
            
            # para acceder a la id de la persona
            # sumamos uno al index dado que la persona seleccionada en la lista es +1
            index = index[0]
            id_cliente = self.lista[index][4]

            self.id_cliente.set(id_cliente)

            if opcion == "Seleccionar":
                self.setear_cliente(persona, id_cliente)
            
                for x in self.widgets:
                    x.destroy()
                
                ventana.destroy()
            
            elif opcion == "Modificar":
                self.crear_cliente(
                    cliente=persona, id_cliente=id_cliente, id_lista=index, main_ventana=ventana)

        else:
            messagebox.showerror(
                title="Error", message="Debes seleccionar un cliente")
            return 0

    def actualizar_lista(self,  index=None):
        # Se le resta 1 dado que el index original es modificado
        # para acceder a la lista
        # si no existe un index, significa que se ingreso un cliente
        # con la opcion agregar cliente

        self.lista_clientes.delete(0, tk.END)
        
        for cliente in self.lista:
            self.lista_clientes.insert(
                tk.END, (cliente[0], cliente[1], cliente[2], cliente[3]))

        self.lista_clientes.activate(index)
        self.lista_clientes.see(index)

    def setear_cliente(self, persona, id_cliente=None):
        
        self.label_cliente.config(
            text=u"Cliente\nNumeración/Lote: %s Calle/Manzana: %s Teléfono: %d Barrio: %s" % (tuple(persona)))

        consulta = verificar_cargo_envio(self.id_cliente.get())

        desactivar_activar_tabs(self.notebook, desactivar=True)

        if consulta:
            id_cargoenvio, self.costo_envio = consulta

            self.total_envio.set(self.costo_envio)
                
            self.label_envio.config(text=ENVIO % self.costo_envio)
            
            self.var_envio.set(id_cargoenvio)

            precio_actual = self.precio_actual.get() + self.costo_envio
            
            self.precio_actual.set(precio_actual)

            self.label_precio_total.config(text=PRECIO_TOTAL % precio_actual)

        
    def encontrar_cliente(self, id_cliente):
        persona = None
        
        self.id_cliente.set(id_cliente)

        for lista in self.lista:
            if lista[4] == id_cliente:
                persona = lista
                self.setear_cliente(persona)
                break

    def destruir(self, ventana, principal=None, opcion=False):
        # se destruye la ventana modificar
        ventana.destroy()

        if not opcion:
            try:
                # se agrega el foco a la ventana cliente
                principal.focus_set()
                principal.grab_set()
                principal.resizable(0, 0)

            except:
                pass
