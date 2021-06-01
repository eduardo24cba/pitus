import tkinter as tk
import sqlite3 as db
import traceback

from tkinter import ttk
from tkinter import messagebox
from archivos.funciones import conectar_db, crear_ventana, centrar
from archivos.constantes import fuente_wid, BG_FRAMES, PRECIO_TOTAL, ENVIO, DESCUENTO
from archivos.caracter import es_num
from archivos.multibox import MultiListbox


def consulta_envio():
    cursor, database = conectar_db()

    if cursor and database:
        try:
            consulta = cursor.execute("SELECT BARRIO, COSTO, idCARGOENVIO FROM CARGOENVIO")

            consulta = consulta.fetchall()
        except db.Error as e:
            messagebox.showerror(
                title="Error", message=u"No se pudo establecer cargo de envío %s funcion consulta_envio" % e)
            return 0
        except Exception:
            messagebox.showerror(
                title="Error", message=u"No se pudo establecer cargo de envío %s funcion consulta_envio" % traceback.format_exc())
            return 0
        else:
            return consulta

        finally:
            database.close()

    else:
        messagebox.showerror("Error", message=u"No se pudo conectar a la base de datos %s funcion consulta_envio" % traceback.format_exc())
        return 0

class Envio:

    def __init__(self, parent):
        self.parent = parent
        
        self.id_cargoenvio = None
        self.label_envio = None
        self.label_precio_total = None
        self.var_precio_total = None
        self.total_envio = None
        self.id_cliente = None
        self.entrega = None

    def opciones_envio(self):
        if not self.id_cliente.get():
            messagebox.showerror(messagebox.ERROR, "Debes seleccionar primeramente un cliente para aplicar un cargo de envío")
            return 0 
        
        if self.entrega.get() == "en puerta":
            messagebox.showerror(messagebox.ERROR, "Si el cliente retira en puerta no puede aplicarse cargo de envío")
            return 0

        pad_x = 10
        pad_y = 10

        ventana = crear_ventana(self.parent, texto="Cargo envio", resizable=True)

        frame = tk.Frame(ventana, bg=BG_FRAMES)

        seleccionar = tk.Button(frame, font=fuente_wid, bg=BG_FRAMES, text="Seleccionar",
                                command=lambda:self.seleccionar_envio(ventana))

        modificar_agregar = tk.Button(frame, font=fuente_wid, bg=BG_FRAMES, text="Agregar o Modificar", 
                                        command=self.agregar_envio)

        boton_quitar_envio = tk.Button(frame, font=fuente_wid, bg=BG_FRAMES, text="Quitar envio", 
                                    command=lambda:self.quitar_envio(ventana))
        
        if self.id_cargoenvio.get():
            boton_quitar_envio.grid(row=0, column=0, pady=pad_y, padx=pad_x, sticky="nsew")
        else:
            seleccionar.grid(       row=0, column=0, pady=pad_y, padx=pad_x, sticky="nsew")
        
        modificar_agregar.grid(row=1, column=0, pady=pad_y, padx=pad_x, sticky="nsew")
        frame.grid()

        centrar(ventana)

    def seleccionar_envio(self, ventana_opciones):

        lista_cargo_envios = consulta_envio()

        #creamos un diccionario con el nombre del barrio como llave y la id como valor
        dic_envios = { envio[0]:envio[2] for envio in lista_cargo_envios}

        if not lista_cargo_envios:
            messagebox.showerror("Error", "No existe envios agregados")
            return 0

        ventana_opciones.destroy()

        ventana = crear_ventana(self.parent, texto="Cargo envio", resizable=True)

        frame = tk.Frame(ventana, bg=BG_FRAMES)

        lista_envios = MultiListbox(frame, (("Barrio", 20), ("Costo", 20)),
                                        alto_ancho=(300, 500), alineacion="nw", selectbackground="red")
        
        #seteamos la variable del cargo de envio con la id del barrio seleccionado.

        seleccionar = tk.Button(frame, text="Seleccionar", font=fuente_wid, 
                                command=lambda: self.setear_envio(lista_envios, dic_envios, ventana))


        for envio in lista_cargo_envios:
            lista_envios.insert(tk.END, (envio[0], envio[1]))

        lista_envios.bind("<Return>", lambda event: self.setear_envio(lista_envios, dic_envios, ventana, event))

        lista_envios.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        seleccionar.grid( row=1, column=0, sticky="nsew", padx=10, pady=10)
        frame.grid()

        centrar(ventana)

    def agregar_envio(self):

        var_costo = tk.IntVar(self.parent)
        
        ventana = crear_ventana(self.parent, texto="Cargo envio", resizable=True)

        frame = tk.Frame(ventana, bg=BG_FRAMES)

        label_barrio = tk.Label(ventana, bg=BG_FRAMES, font=fuente_wid, text="Barrio")

        barrio = tk.Entry(ventana, bg=BG_FRAMES, font=fuente_wid)

        label_precio = tk.Label(ventana, bg=BG_FRAMES, font=fuente_wid, text="Costo")

        costo = tk.Entry(ventana, bg=BG_FRAMES, font=fuente_wid, textvariable=var_costo)

        aceptar = tk.Button(ventana, bg=BG_FRAMES, font=fuente_wid, text="Aceptar",
        command=lambda:self.guardar_envio(ventana, costo, barrio))

        label_barrio.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
        barrio.grid(      row=0, column=1, sticky="nsew", pady=10, padx=10)
        label_precio.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        costo.grid(       row=1, column=1, sticky="nsew", pady=10, padx=10)
        aceptar.grid(     row=2, column=0, sticky="nsew", pady=10, padx=10)
        frame.grid()

        centrar(ventana)

    def quitar_envio(self, ventana):
        consulta = messagebox.askyesno("Consulta envio", "Esta a punto de quitar el envio elegido para este cliente."+
                                    "Esto puede afectar a otros pedidos de este cliente que ya posean cargo de envio"+
                                    "¿Desea continuar?")

        if not consulta:
            return 0
        else:
            result = self.aplicar_o_quitar_envio_a_cliente(quitar=True)
            if not result:
                return 0

        #actualizamos labels y monto
        total = self.var_precio_total.get()
        
        total = total - self.total_envio.get()

        self.total_envio.set(0)

        self.var_precio_total.set(total)
        
        self.id_cargoenvio.set(0)

        self.label_precio_total.config(text=PRECIO_TOTAL % total)
        
        self.label_envio.config(text=ENVIO % self.total_envio.get())
        
        messagebox.showinfo("Aviso", "Envio quitado exitosamente")
        
        ventana.destroy()

    def setear_envio(self, lista_envios, dic_envios, ventana, event=None):
        #con el diccionario creado previamente, accedemos al valor que es la id del barrio
        #en base a lo seleccionado en la multilistbox
        
        #obtenemos la lista que contiene el barrio y el costo
        seleccion = lista_envios.get(lista_envios.curselection())

        #accedemos a la id en el diccionario y seteamos la variable que viene desde fuera
        self.id_cargoenvio.set(dic_envios.get(seleccion[0]))

        #extraemos el precio total y sumamos el cargo de envio
        total = self.var_precio_total.get()

        total = total + seleccion[1]

        self.label_precio_total.config(text=PRECIO_TOTAL % total)

        self.var_precio_total.set(total)

        #seteamos la variable que tiene el costo de envio del barrio
        self.total_envio.set(seleccion[1])

        self.label_envio.config(text=ENVIO % seleccion[1])
        
        ventana.destroy()

    def aplicar_o_quitar_envio_a_cliente(self, quitar=False, cursor=None):
        #la database ingresa desde la interfaz pedidos 
        #no se aplica un commit aca, se lo aplica cuando se guarda el pedido
        
        database = None

        #si no recibimos cursor desde afuera, significa que ingreso por otro lado
        if not cursor:
            cursor, database = conectar_db()
        
        #si hay cursor, significa que se conecto a la base de datos
        if cursor:
            try:
                if not quitar:
                    cursor.execute("UPDATE CLIENTE SET idCARGOENVIO='%d' WHERE idCLIENTE='%d'" % (self.id_cargoenvio.get(), self.id_cliente.get()))
                else:
                    cursor.execute("UPDATE CLIENTE SET idCARGOENVIO='0' WHERE idCLIENTE='%d'" % self.id_cliente.get())
            
            except Exception:
                messagebox.showerror(messagebox.ERROR, "%s funcion aplicar_o_quitar_envio_a_cliente" % traceback.format_exc())
                return 0 

            except database.Error as e:
                messagebox.showerror(messagebox.ERROR, "Error en la base de datos %s funcion aplicar_o_quitar_envio_a_cliente" % e)
                return 0

            else:
                #si existe database signifca que se conecto por la funcion conectar_db
                if database:
                    database.close()
                return 1
        


    def guardar_envio(self, ventana, costo, barrio):

        cursor, database = conectar_db()

        try:
            if not es_num(costo.get()):
                messagebox.showerror("Error", "El campo costo solo acepta numero")
                return 0
        
        except Exception:
            messagebox.showerror("Error", "El campo costo solo acepta numero funcion guardar_envio %s" % traceback.format_exc())
            return 0

        if not int(costo.get()):
            messagebox.showerror("Error", "DEbes ingresar un costo")
            return 0

        if not barrio.get():
            messagebox.showerror("Error", "Debes ingresar un barrio")
            return 0

        if cursor and database:

            try:
                cursor.execute("INSERT INTO CARGOENVIO (BARRIO, COSTO) VALUES (?, ?)", (barrio.get(), int(costo.get())))
                cursor.connection.commit()
                
                messagebox.showinfo("Aviso", "Envio agregado con exito")
                ventana.destroy()
            except db.Error:
                messagebox.showerror("Error", "Error al guardar envio %s funcion guardar_envio" % traceback.format_exc())
                return 0
            except Exception:
                messagebox.showerror("Error", "Error al guardar envio %s funcion guardar_envio" % traceback.format_exc())
                return 0

            finally:
                database.close()
        else:
            messagebox.showerror("Error", message=u"No se pudo conectar a la base de datos %s" % traceback.format_exc())
            return 0 

