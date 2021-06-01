from tkinter import ttk
from tkinter import messagebox
from archivos.caracter import alfa_num, caracter, es_num
from archivos.constantes import lista_mes, dias_fin_de_mes
import sqlite3 as db
import time, traceback
import os

import tkinter as tk

#Diccionario Cliente clave:Nombre y apellido. Values: telefono, direccion, id.
#Diccionarios Bebida clave:Bebida values:Precio, id.
#Diccionarios Menu clave:Menu values:Precio, id.
#Diccionarios Postre clave:Postre values:Precio, id.


def crear_ventana(root, texto=None, icono=None, dimensiones=None, resizable=None, bg=None):
    #Funcion que crea una ventana toplevel con dimensiones otorgadas por el usuario
    #y sin ellas, la ventana siempre se centra gracias a Dios.
    #dimensiones = (alto,ancho)
    #focus_set() and grab_set() hacen que la ventana tenga siempre el focus
    ventana_nueva = tk.Toplevel(root)
    
    if resizable:
        ventana_nueva.resizable(0,0)
        ventana_nueva.focus_set()
        ventana_nueva.grab_set()
    if icono:
        icono_ico = icono +'.ico'
        try:
            ventana_nueva.iconbitmap(os.path.join("iconos\\%s" % icono_ico))
        except Exception as e:
            print(e)
            return False
    if not dimensiones:
        ventana_nueva.geometry()
    else:
        posx  = (root.winfo_screenwidth()  - dimensiones[0])  / 2
        posy  = (root.winfo_screenheight() - dimensiones[1]) / 2
        ventana_nueva.geometry("%dx%d+%d+%d" % (dimensiones[0], dimensiones[1], posx, posy))

    if texto:
        ventana_nueva.title(texto)

    if bg:
        ventana_nueva.config(bg=bg)
    return ventana_nueva

def validar(datos, opcion, ):
    #validamos los datos de los productos que agregamos o modificamos
    campos = (opcion, "Precio", "Tipo" if opcion == "bebida" else "Ingredientes")

    clausula1 = "Debes ingresar letras en el campo %s"
    clausula2 = "Debes ingresar números en el campo %s"
    clausula3 = "Debes ingresar números y letras solamente en el campo %s\nNo están permitidos los caracteres especiales."
    
    a, b, c = datos[0].get(), datos[1].get(), datos[2].get("1.0","end-1c")

    
    if not caracter(a, True):
        messagebox.showerror(title="Error", message=clausula1 % campos[0])
        return 0
    elif not es_num(b):
        messagebox.showerror(title="Error", message=clausula2 % campos[1])
        return 0
    elif not alfa_num(c, True):
        messagebox.showerror(title="Error", message=clausula3 % campos[2])
        return 0
    else:
        a = caracter(a,True)
        b = int(b)
        c = alfa_num(c,True)
        
        return a, b, c

def validar_cliente_viejo(datos):
    #haremos una nueva funcion
    campos = ("Lote", "Manzana", "Teléfono", "Barrio") 
    #si los datos que nos pasan en la ventana cliente
    #no estan permitidos, retornamos false.
    for x in range(len(datos[:3])):
        if not es_num(datos[x].get()):
            messagebox.showerror(title="Error", message="Debes ingresar números en el campo %s" % campos[x])
            return 0

    if not alfa_num(datos[3].get("1.0","end-1c"), True):
        messagebox.showerror(title="Error",
                             message="Debes ingresar números y letras solamente en el campo %s\nNo están permitidos los caracteres especiales." % campos[3])
        return 0
    else:
        a, b, c, d = datos[0].get(), datos[1].get(), datos[2].get(), datos[3].get("1.0","end-1c")
        a = int(a)
        b = int(b)
        c = int(c)
        d = alfa_num(d, True)

        return a, b, c, d

def validar_cliente(datos):
    #validamos que todos
    campos = ("Numeracion/Lote", "Calle/Manzana", "Teléfono", "Barrio")

    for x in range(len(datos[:3])):
        if not len(datos[x].get()):
            messagebox.showerror(title="Error", message="Debes rellena el campo" % campos[x])
            return 0

    if not len(datos[3].get("1.0","end-1c")):
        messagebox.showerror(title="Error",
                             message="Debes rellenar el campo" % campos[3])
        return 0

    else:
        numeracion_lote, calle_manzana, telefono, barrio = datos[0].get(), datos[1].get(), datos[2].get(), datos[3].get("1.0","end-1c")

        numeracion_lote = " ".join(numeracion_lote.split())
        calle_manzana = " ".join(calle_manzana.split())
        telefono = "".join(telefono.split())
        barrio = " ".join(barrio.split())

        if not es_num(telefono):
            messagebox.showerror(title="Error", message=u"Debes ingresar solamente números en el campo teléfono")
            return 0

        telefono = int(telefono)
        
        return numeracion_lote, calle_manzana, telefono, barrio
    
def conectar_db():
    try:
        database = db.connect("pedidos.db")
        cursor = database.cursor()
    except:
        return messagebox.showerror(title="Error", message=MENSAJE_DB)
    else:
        return cursor,database

def anio_biciesto(anio):
    #si el anio es biciesto return True
    #se entiende que si no es biciesto
    #saltara esa linea y retornara falso
    if anio % 4 == 0 and (anio % 100 !=0 or anio % 400 == 0):
        return True
    return False

def consultar_fin_de_mes(mes, anio):
        index_mes= lista_mes.index(mes)
        biciesto = anio_biciesto(anio)
        if mes == "Febrero" and biciesto:
            #biciesto
            mes = dias_fin_de_mes[index_mes] + 1
        else:
            mes = dias_fin_de_mes[index_mes]               
        return mes

def obtener_fecha(fecha=False, mes=False, anio=False):
    #almacenamos la fecha como YYYY-MM-DD = 2019-04-03
    if fecha:
        try:
            fecha = time.strftime("%Y-%m-%d")
        except:
            messagebox.showerror(title="Error",
                                 message="Imposible obtener fecha, error 001")
            return 0
        else:
            return fecha
    elif mes:
        try:
            mes = time.strftime("%m")
        except:
            messagebox.showerror(title="Error",
                                 message="Imposible obtener mes, error 001")
            return 0
        else:
            return mes
    elif anio:
        try:
            anio = time.strftime("%Y")
        except:
            messagebox.showerror(title="Error",
                                 message="Imposible obtener anio, error 001")
            return 0
        else:
            return anio
    else:
        messagebox.showerror(title="Error",
                             message="Debes ingresar argumento mes, anio, o fecha")
        return 0

def desactivar_botones(botones):
    for boton in botones:
        boton.config(state='disabled')

def activar_botones(botones):
    #si el boton cliente esta deshabilitado
    #significa que se realizo otro pedido por el mismo cliente
    #se habilita al apretar guardar pedido
    #el primer boton es buscar_cliente

    for boton in botones:
        boton.config(state='normal')    

def comprobar_si_hay_pedido(pedido):
    return True if pedido else False

def invertir_fecha(fecha, retornar_separado=False, caracter="-"):
    #si coloco el caracter me tira error si pongo entre comillas funciona
    #no entiendo...
    fecha = tuple(fecha.split("-")[::-1])

    if caracter == "-":
        fecha_str = "%s-%s-%s" % fecha
    else:
        fecha_str = "%s/%s/%s" % fecha
    return fecha_str if not retornar_separado else fecha

def reset_grafica(desde, hasta, ccbox1, ccbox2, var_menu, var_opcion,
                  boton_desde, boton_hasta, mes_elegido, anio_elegido,
                  var_estado):
    boton_desde.config(text="Desde", state="normal")
    boton_hasta.config(text="Hasta", state="disabled")
    mes_elegido.set('0')
    anio_elegido.set('0')
    var_estado.set("normal")
    default_ccbox(lista=(ccbox1, ccbox2, var_menu, var_opcion, desde, hasta), valor="")

def retornar_fuente_responsive(ancho):
    #obtenemos el ancho - alto de una ventana o frame
    #y en base a eso sacamos una distancia dada

    #print("el ancho es ", ancho)
    
    if ancho >= 1100 and ancho <= 1290:
        #print("el ancho esta en el rango definido: ", ancho)
        fuente_responsive = ('Tahoma', 12, 'bold')
    
    elif ancho >= 900 and ancho <= 1100:
        #print("el ancho esta en el rango definido: ", ancho)
        fuente_responsive = ('Tahoma', 11, 'bold')

    elif ancho >= 800 and ancho <= 900:
        #print("el ancho esta en el rango definido: ", ancho)
        fuente_responsive = ('Tahoma', 9, 'bold')
    
    elif ancho >=700 and ancho <=800:
        #print("el ancho esta en el rango definido: ", ancho)
        fuente_responsive = ('Tahoma', 8, 'bold')

    elif ancho >=600 and ancho <= 700:
        #print("el ancho esta en el rango definido: ", ancho)
        fuente_responsive = ('Tahoma', 7, 'bold')
    else:
        fuente_responsive = ('Tahoma', 10, 'bold')
   
    return fuente_responsive

def centrar(ventana):
    ventana.update()
    ventana.update_idletasks()
    posx = (ventana.winfo_screenwidth() - ventana.winfo_width()) / 2
    posy = (ventana.winfo_screenheight()- ventana.winfo_height()) / 2
    ventana.geometry("+%d+%d" % (posx, posy))

def marcar_activo(boton, botones):
        #se les quita el borde al que este marcado como sunken
        for x in botones:
            if x.cget('relief') == "sunken":
                x.config(relief=tk.RAISED)

        #se cambia el borde del boton a pressed
        boton.config(relief=tk.SUNKEN)

def rellenar_diccionario(diccionario, lista_productos=None, opcion=None, nuevo_item=False, item=None, var=None):
    #se recibe un diccionario y se rellena con los datos extraidos de la consulta
    #si el diccionario tiene items, no es necesario consultar la base de datos nuevamente
    #si se agrego un nuevo producto, entonces debemos insertarlo en el diccionario.
    
    if not diccionario.items():
        #si no tiene items entonces es la primera vez
        cursor, database = conectar_db()

        consulta = cursor.execute(
            "SELECT PRODUCTO, PRECIO, ROWID FROM PRODUCTO WHERE TIPOPRODUCTO='%s' " % (
                opcion
                )                    )
                    
        consulta = consulta.fetchall()

        #no hay nada en la base de datos
        if not consulta:
            messagebox.showinfo(
                "Info", "No se ha guardado %s en la base de datos, agrega para continuar." % opcion.capitalize())
            return 0

        for producto in consulta:
            diccionario[producto[0]] = producto[1:]
        
        database.close()
        
    if nuevo_item:
        #si existe un nuevo item, existe una variable para verificar
        if item[0] in diccionario.keys():
            messagebox.showerror(messagebox.ERROR, "ya existe ese producto")
            var.set(1)
            return 0

        else:
            #si el producto existia la variable se seteo a 1
            #modifico el producto, entonces ya no hay error
            #seteamos a 0 para poder continuar
            if var.get():
                var.set(0)

            diccionario[item[0]] = item[1:]

    if lista_productos:
        #ordenamos el diccionario y este se convierte a lista, evitamos eso anteponiendo dict
        diccionario = dict(sorted(diccionario.items()))

        for producto, precio in diccionario.items():
            lista_productos.insert("end", (producto, precio[0]))


def extraer_id(diccionarios, key):
    for dic in diccionarios:
        if key in dic.keys():
            return dic.get(key)[1]

def destruir_hijos(frame):
    for hijo in frame.winfo_children():
        hijo.destroy()

def desactivar_activar_tabs(notebook, desactivar):
    """
    desactivar es de tipo booleano
    """
    if desactivar:
        notebook.tab(1, state="disabled")
        notebook.tab(2, state="disabled")
        notebook.tab(3, state="disabled")
    else:
        notebook.tab(1, state="normal")
        notebook.tab(2, state="normal")
        notebook.tab(3, state="normal")

def crear_progressbar(parent, alto, ancho, bg):
    frame = tk.Frame(parent, width=ancho, height=alto, bg=bg)

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

    actualizar_progressbar(parent, progressbar, frame)

def actualizar_progressbar(parent, progressbar, frame):
    #se llama 2 veces esto por eso sale error, solucionar
        
    if progressbar["value"] < 100:
        valor = progressbar["value"] 
        progressbar["value"] = valor + 20
            
        parent.update_idletasks()

        parent.after(100, lambda: actualizar_progressbar(parent, progressbar, frame))
    else:
        progressbar.destroy()
        frame.destroy()

        print("termino el progresbar")

        return True