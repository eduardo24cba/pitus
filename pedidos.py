#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import tkinter as tk

#calle 23 lote 23 error entrega

from tkinter import ttk
from tkinter import messagebox

#from archivos.caja import caja
from archivos.crear_pedido import interfaz_crear_pedido
from archivos.constantes import BG_PEDIDOS, BG_FRAMES
from archivos.funciones import destruir_hijos, desactivar_activar_tabs
from archivos.lista_pedidos import crear_lista_pedidos

from archivos.cliente import Cliente
from archivos.productos import Producto
from archivos.cargo_envio import Envio
from archivos.caja import caja

from PIL import Image, ImageTk, IcoImagePlugin
Image._initialized=2

#el progresbar se debe mover de costado a costado, una vez que la pantalla se cargo
#informar que se detenga y mostrar los elementos


#cantidad = variable.get() - cantidad_producto
#AttributeError: 'NoneType' object has no attribute 'get'
#error en cambiar estado pedidos, verificar

#c.execute(" select a.fecha, c.tipocuenta, c.debe, c.haber, m.tipomovimiento
# from movimientocontable m inner join asientocontable a on a.idASIENTO == m.idASIENTO inner join 
# cuenta c on c.idCUENTA == m.idCUENTA where a.fecha='2021-05-17'" )

#debemos ver bien como trabaja sqlite con las conexiones porque sino 
#nos aparece database locked.

#cada vez que cambiemos de pantalla, debemos destruir los widgets de la pantalla anterior
#al parecer quedan vivos por un rato

#los productos agregados deben ser unicos, debemos poner una condicion, no queremos
#que se agregen dos papas fritas chicas
#agregar codigo de producto para mejorar esto


#Comienzo del proyecto enero 2018

#Entregado a prueba 13/08/2019

#actualizado 13/08/2019 23:29


#funciones, informacion que faltan

#---Cosas a corregir/mejorar

#---Migrar a mysql

#---Cambiar la grafica que se muestra por una funcion lineal
####agregar la cantidad de pedidos que se despacho, mostrar en la grafica la cantidad total

ANCHO = 240
ALTO = 100

imagenes = [Image.open(os.path.join(os.path.abspath("iconos"), "pedidos despachados.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "pedidos.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "deudas.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "ColGB.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "buscar cliente.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "caja.ico")),
            Image.open(os.path.join(os.path.abspath("iconos"), "more.ico")),
            ]

class Pedido(tk.Tk):

    fuente_menu = ('Futura Hv BT, Heavy	',12)
    
    #la orientacion del texto respecto al icono
    #panel izquiedo de opciones
    orientacion = "top"

    #tamanio de los iconos
    tamanio_iconos = (30,30)
    
    def __init__(self):
        ##############################################################
        tk.Tk.__init__(self)
        self._offsetx = 0
        self._offsety = 0
        self.bg_frame = "#646184"

        #imagenes
        self.imagen_pedidos = ImageTk.PhotoImage(imagenes[1].resize(self.tamanio_iconos, Image.ANTIALIAS))
        self.imagen_deudas  = ImageTk.PhotoImage(imagenes[2].resize(self.tamanio_iconos, Image.ANTIALIAS))
        #self.imagen_gota    = ImageTk.PhotoImage(imagenes[3].resize((80,80), Image.ANTIALIAS))
        
        self.imagen_caja = ImageTk.PhotoImage(imagenes[5].resize(self.tamanio_iconos, Image.ANTIALIAS))
        self.imagen_more = ImageTk.PhotoImage(imagenes[6].resize(self.tamanio_iconos, Image.ANTIALIAS))

        self.imagen_despachados = ImageTk.PhotoImage(imagenes[0].resize(self.tamanio_iconos, Image.ANTIALIAS))
        self.imagen_buscar_cliente = ImageTk.PhotoImage(imagenes[4].resize((15,15), Image.ANTIALIAS))

        #animacion con pestanias
        self.notebook = None

        #inicializamos las clases
        self.clase_cliente = Cliente(self)
        self.clase_producto = Producto(self)
        self.clase_envio = Envio(self)
        
        #frames para las oppciones en notebook
        self.frame_nuevo_pedido = None
        self.frame_en_proceso = None
        self.frame_preparados = None
        self.frame_delivery = None

        #esta variable nos mostrara donde se encontraba el usuario anteriormente
        self.frame_anterior = None
        
        #establecemos un tamanio de ventana que se adaptara a todos los monitores de pantalla
        #calculamos el maximo de pantalla y le restamos la cantidad que deseamos que tenga la pantalla
        self.ancho = self.winfo_screenwidth() - ANCHO
        self.alto = self.winfo_screenheight() - ALTO
        self.posx = (self.winfo_screenwidth() - self.ancho) / 2
        self.posy = (self.winfo_screenheight() - self.alto) / 2
        
        #atach
        self.frame_accesos = tk.Frame(self, bg="red")

        self.frame_accesos.grid_propagate(0)

        self.frame_tareas = tk.Frame(self, bg="green")

        self.frame_tareas.grid_propagate(0)

        #botones inicio
        #mostramos los pedidos en proceso, delivery y finalizados.
        alto_botones = 80

        #----------------------------------------------Pedidos---------------------------------------------#
        self.boton_pedidos = tk.Button(self.frame_accesos, text="Pedidos", image=self.imagen_pedidos, font=self.fuente_menu,
                                    justify=tk.LEFT, compound=self.orientacion, fg="#D99551", bg="#646184", relief=tk.RAISED,
                                    height=alto_botones)


        #----------------------------------------------Pedidos despachados---------------------------------------------#
        #self.boton_pedidos_despachados = tk.Button(self.frame_accesos, text="Pedidos\nDespachados", image = self.imagen_despachados,
        #                                        font=self.fuente_menu, justify=tk.LEFT, compound=self.orientacion, fg="#D99551", bg="#646184",
        #                                        relief=tk.RAISED, height=alto_botones,)


        #----------------------------------------------Deudas---------------------------------------------#
        #self.boton_deuda = tk.Button(self.frame_accesos, height=alto_botones, text="Deudas", image = self.imagen_deudas, font=self.fuente_menu,
        #                          justify=tk.LEFT, compound=self.orientacion, fg="#D99551", bg="#646184", relief=tk.RAISED)


        #----------------------------------------------Caja---------------------------------------------#
        self.boton_caja = tk.Button(self.frame_accesos, height=alto_botones, text="Caja", image = self.imagen_caja, font=self.fuente_menu,
                                 justify=tk.LEFT, compound=self.orientacion, fg="#D99551", bg="#646184", relief=tk.RAISED)


        #sabremos que boton esta presionado por que el relieve no sera raised
        self.botones = [self.boton_pedidos, self.boton_caja]

        pad_x = 2
        pad_y = 2
        
        self.boton_pedidos.grid(row=0, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
        #self.boton_pedidos_despachados.grid(row=1, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
        #self.boton_deuda.grid(row=2, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
        self.boton_caja.grid(row=1, column=0, sticky="nsew", padx=pad_x, pady=pad_y)
        
        self.frame_accesos.grid(row=0, column=0,  pady=10)
        self.frame_tareas.grid( row=0, column=1,  pady=10)
        

        """
        self.frame_accesos.grid_columnconfigure(0, weight=0)
        self.frame_accesos.grid_rowconfigure(0, weight=0)
        self.frame_accesos.grid_columnconfigure(1, weight=0)
        self.frame_accesos.grid_rowconfigure(1, weight=0)
        self.frame_accesos.grid_columnconfigure(2, weight=0)
        self.frame_accesos.grid_rowconfigure(2, weight=0)
        self.frame_accesos.grid_columnconfigure(3, weight=0)
        self.frame_accesos.grid_rowconfigure(3, weight=0)
        """
        
        self.geometry("%dx%d+%d+%d" % (self.ancho, self.alto, self.posx, self.posy-50))
      
        #color de fondo, letra, etc.
        self.config(bg="#646184")
        self.iconbitmap("@/" + os.path.join(os.path.abspath("iconos"), "ColGB.xbm"))
        self.title("ColGB - Programa pedidos")

        style = ttk.Style()
        if sys.platform == "win32":
            style.theme_use('winnative')

        style.configure('TNotebook', background=BG_PEDIDOS)
        style.configure('TNotebook.Tab', background=BG_PEDIDOS)
        #style.configure('TNotebook.Tab', foreground="#d7d7d7")

        #self.button = Button(self, image = self.imagen_gota, bg="#646184", relief=FLAT)
        #self.button.grid(row=100, column=0, sticky="se", pady=450)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        #self.resizable(0,0)

        self.estado = True
        
        self.bind("<Escape>", self.maximiza)
        #self.maximiza()
        #actualizamos el tamanio del widget
        
        self.update()
        self.update_idletasks()

        #obtenemos el ancho en pixeles del boton con la frase mas grande y le damos un margen de 6
        #que se suma al padx que ya tienen los botones
        self.ancho_frame_accesos = self.boton_pedidos.winfo_reqwidth() + 6

        self.frame_accesos.configure(width=self.ancho_frame_accesos, height=self.winfo_height())
        self.frame_tareas.configure( width=self.winfo_width() - self.ancho_frame_accesos,
                                                           height=self.winfo_height())

         #---------------asignacion de funciones a botones----------------#
        self.boton_pedidos.configure(command=lambda boton=self.boton_pedidos: self.pedidos(boton))
        self.boton_caja.configure(   command= lambda: caja(self, self.frame_tareas, self.ancho_frame_accesos, self.notebook,
                                                           self.boton_caja, self.botones))

        #self.boton_pedidos_despachados.configure(command=lambda boton=self.boton_pedidos_despachados: self.pedidos_despachados(boton))

        #self.boton_deuda.configure(command=lambda boton=self.boton_deuda: self.deudas(boton))



         #si la ventana cambia el tamaño se dispara este evento

        self.after(1000, self.aplicar_bind)

        #hacer transparencia
        #self.attributes("-alpha", 0.)

    def maximiza(self, event=None):
        self.attributes("-fullscreen", self.estado)

        if self.estado:
            self.estado = False

        elif not self.estado:
            self.estado = True

        self.update()
        self.update_idletasks()
        
        #debemos aplicar los cambios en 50 mm para darle tiempo a actualizar el tamaño
        self.after(50, lambda:self.frame_accesos.config(height=self.winfo_height()))

        self.after(50, lambda:self.frame_tareas.configure(width=self.winfo_width() - self.ancho_frame_accesos,
                                                          height=self.winfo_height()))

        if self.notebook:
            self.after(50, lambda:self.notebook.configure(width=self.winfo_width() - (self.frame_accesos.winfo_width() - 40),
                                                          height=self.winfo_height()))



    def on_close(self):
        #debemos detener el mainloop
        #destruimos luego la ventana.
        #si accedimos a caja y existio caja mensual
        #entonces se creo una grafica, la variable plot tendra un grafico
        #si no tiene grafico, no se inicio el mainloop de la ventana
        
        self.quit()
        self.destroy()

    def aplicar_bind(self):
        self.bind("<Configure>", lambda event: self.actualizar_elementos(event))


    def actualizar_elementos(self, event):

        if self.alto != self.winfo_height() or self.ancho != self.winfo_width():
            print ("cambio el alto o el ancho")
            print("####")


    def pedidos(self, boton):
        boton.config(relief=None)
        #dependiendo del caracter que seleccionemos con underline
        #podremos acceder a las pestania por medio de alt+ esa letra.

        if self.notebook:
            #esta creada la notebook, entonces preguntamos si esta activa
            #si esta activa, significa que presiono el boton pedidos
            #no haremos nada

            if self.notebook.index(self.notebook.select()):
                pass
        else:
            #creamos por primera vez el notebook y las tabs
            self.crear_frames(boton)

    def crear_frames(self, boton):

        self.notebook = ttk.Notebook(self.frame_tareas)

        self.clase_cliente.notebook = self.notebook
        self.clase_producto.notebook = self.notebook
        
        self.frame_nuevo_pedido = tk.Frame(self.notebook, name="nuevo pedido", bg=BG_FRAMES)
        self.frame_en_proceso   = tk.Frame(self.notebook, name="proceso", bg=BG_FRAMES)
        self.frame_preparados   = tk.Frame(self.notebook, name="preparado", bg=BG_FRAMES)
        self.frame_delivery     = tk.Frame(self.notebook, name="delivery", bg=BG_FRAMES)
            
        self.frame_nuevo_pedido.grid(sticky="nsew")
        self.frame_en_proceso.grid(  sticky="nsew")
        self.frame_preparados.grid(  sticky="nsew")
        self.frame_delivery.grid(    sticky="nsew")
                
        self.notebook.add(self.frame_nuevo_pedido, padding=2, underline=2, text="Crear pedido")
        self.notebook.add(self.frame_en_proceso,   padding=2, underline=2, text="Pedidos en proceso")
        self.notebook.add(self.frame_preparados,   padding=2, underline=2, text="Pedidos preparados")
        self.notebook.add(self.frame_delivery,     padding=2, underline=2, text="Pedidos delivery")

        #self.notebook.bind("<<NotebookTabChanged>>", 
        #                  lambda e: self.crear_progressbar(boton=boton, alto=alto, ancho=ancho, event=e))

        self.notebook.bind("<Button-1>", lambda e: self.redireccionar(boton=boton, event=e))

        self.after(50, lambda:self.notebook.configure(width=self.winfo_width() - (self.frame_accesos.winfo_width() - 40),
                                                      height=self.winfo_height()))

        #cuando se inicia por primera vez significa que presiono crear frames
        
        self.redireccionar(boton=boton, event=None)

        self.notebook.grid(row=0, column=0, padx=5)

        self.notebook.grid_propagate(0)
        
    def redireccionar(self, boton, event=None):
        #boton se pasa para que marque que en opcion estamos
        #verificar este error al presionar el boton pedido: 
        #AttributeError  'Button' object has no attribute 'widget'

        #sabemos que tab presiono, puede venir de un evento al presionar una pestaña o puede ser que
        #ingreso por primera vez cuando creamos los frames y se redirecciono.
        
        if event:
            tab_presionada = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)

        else:
            tab_presionada = 0

        if self.frame_anterior == "nuevo pedido":
            destruir_hijos(self.frame_nuevo_pedido)
        
        elif self.frame_anterior == "en proceso":
            destruir_hijos(self.frame_en_proceso)
        
        elif self.frame_anterior == "preparado":
            destruir_hijos(self.frame_preparados)
        
        elif self.frame_anterior == "delivery":
            destruir_hijos(self.frame_delivery)
        
        else:
            #es none
            pass


        if tab_presionada == 0:

            self.frame_anterior = "nuevo pedido"

            interfaz_crear_pedido(self, self.frame_nuevo_pedido, boton,
                                  self.botones, self.clase_cliente,
                                  self.clase_producto, self.clase_envio,
                                  self.notebook, self.ancho_frame_accesos,
                                  self.frame_tareas)
        
        elif  tab_presionada == 1:
            self.frame_anterior = "en proceso"

            self.after(100, lambda: crear_lista_pedidos(self.frame_en_proceso, self.frame_tareas, self.notebook, self, "en proceso",self.ancho_frame_accesos, True))
        
        elif  tab_presionada == 2:

            self.frame_anterior = "preparado"

            self.after(100, lambda: crear_lista_pedidos(self.frame_preparados, self.frame_tareas, self.notebook, self, "preparado", self.ancho_frame_accesos, False))

        else:
            # tab_presionada == 3
            #event.widget.tab(event.widget.select(), "text") == "Pedidos delivery":

            self.frame_anterior = "delivery"

            self.after(100, lambda: crear_lista_pedidos(self.frame_delivery, self.frame_tareas, self.notebook, self, "en camino", self.ancho_frame_accesos, False))

    def crear_progressbar(self, boton=None, event=None):
        #si hay event significa que no es un nuevo pedido
        #el event pudo ingresar por que cambio de tab o porque ingresamos por primera vez
        #y seteamos la tab a 0
        tab_presionada = 0

        ancho = self.winfo_width() - (self.frame_accesos.winfo_width() - 40)
        alto = self.winfo_height()

        if event:
            parent = event.widget
            
            #nombre de la tab presionada
            #event.widget.tab(event.widget.select(), "text")
            
            #sabemos que tab presiono
            tab_presionada = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        else:
            #si no hay evento, lo estamos redirigiendo nosotros
            parent = self.notebook

        if not self.clase_cliente.id_cliente.get() and not self.clase_producto.producto_seleccionado.get():

            frame = tk.Frame(parent, width=ancho, height=alto, bg=self.bg_frame)

            frame.grid_propagate(0)
            
            progressbar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")

            progressbar["value"] = 0

            #centramos el progresbar con estas lineas        
            progressbar.grid_rowconfigure(1, weight=1)
            progressbar.grid_columnconfigure(1, weight=1)
            
            #estas tambien
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            frame.grid(row=0, column=0, sticky="nsew")

            progressbar.grid()

            self.mostrar_progressbar(progressbar, tab_presionada, boton, frame, event)

        else:
            
            consulta = messagebox.askyesno(messagebox.INFO, "Esta apunto de cambiar de pantalla y tiene datos sin guardar\n"+
                                                            "¿Desea continuar?")
            
            if consulta:
                
                self.clase_cliente.id_cliente.set(0)
                
                self.clase_producto.producto_seleccionado.set(0)
                
                desactivar_activar_tabs(self.notebook, desactivar=False)
                
                #self.redireccionar(tab_presionada=tab_presionada, boton=boton)

                #destruimos porque aun sigue activo
                destruir_hijos(self.frame_nuevo_pedido)

                return
            
            else:
                return 0

    def mostrar_progressbar(self, progressbar, tab_presionada, boton, frame, event):
        #se llama 2 veces esto por eso sale error, solucionar
        
        if progressbar["value"] < 100:
            valor = progressbar["value"] 
            progressbar["value"] = valor + 20
            
            self.update_idletasks()

            self.after(100, lambda:self.mostrar_progressbar(progressbar, tab_presionada, boton, frame, event))
        else:
            progressbar.destroy()
            frame.destroy()
            #aca preguntamos que pestaña fue presionada y ejecutamos su funcion

            #self.after(100, lambda:self.redireccionar(tab_presionada=tab_presionada, boton=boton))

            return
            
if __name__=='__main__':
    pedido = Pedido()
    pedido.mainloop()
