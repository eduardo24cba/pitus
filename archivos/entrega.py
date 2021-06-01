from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as db
from archivos.funciones import conectar_db, crear_ventana, centrar
from archivos.constantes import fuente_wid, fuente_botones, BG_COMANDA_ENTREGA, BG_COMANDA_DELIVERY, BG_BOTONES_DEUDA, FG_BOTON_DEUDA, ENVIO
import traceback
import time

def verificar_envio(id_cliente, entrega, cursor):
    
    if cursor:
        try:
            consulta = cursor.execute("""SELECT pe.TIPOENTREGA FROM PEDIDO pe
                                         INNER JOIN CLIENTE c ON pe.idCLIENTE = c.idCLIENTE
                                         WHERE c.idCLIENTE='%d' AND pe.ESTADO IN ('en proceso','preparado', 'en camino', 'en puerta')""" % id_cliente)
            consulta = consulta.fetchone()

            print("la consulta", consulta)
        except db.Error as e:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        except Exception as e:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        else:
            if consulta:
                print("verificamos envio", consulta, entrega)
                if entrega in consulta:
                    return 1
                else:
                    return 0
            else:
                print("no hay consulta")

def verificar_cargo_envio(id_cliente):
    cursor, database = conectar_db()
    
    if cursor and database:
        try:
            consulta = cursor.execute("""SELECT cl.idCARGOENVIO, cr.COSTO FROM CLIENTE cl
                                         INNER JOIN CARGOENVIO cr ON cl.idCARGOENVIO = cr.idCARGOENVIO
                                         WHERE cl.idCLIENTE='%d'""" % id_cliente)
            consulta = consulta.fetchone()
        
        except db.Error:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        except Exception:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        else:
            if consulta:
                return consulta
            else:
                return 0 
        
        finally:
            database.close()

def cambiar_entrega(id_cliente, entrega, cursor):
    """
    datos cliente: Lote, Mza
    """

    consulta = messagebox.askyesno("Consulta entrega", "Se va a cambiar la entrega de todos los pedidos a %s \n¿Desea continuar?" % entrega)

    if consulta:
        cambiar_entrega_pedidos(entrega, id_cliente, cursor)
    else:
        return 0 
    #label_nombres  = Label(nueva_ventana, justify=LEFT, font=fuente_wid, text=u"Calle/Lote: %s" % datos_cliente[0] )
    

def verificar_pedidos(id_cliente, entrega, cursor):
    
    if cursor:
        try:
            consulta = cursor.execute("""SELECT pe.ESTADO FROM PEDIDO pe
                                         INNER JOIN CLIENTE c ON pe.idCLIENTE = c.idCLIENTE
                                         WHERE c.idCLIENTE='%d'""" % id_cliente)

            consulta = consulta.fetchall()

            for estado in consulta:
                if entrega == "eelivery":
                    if estado[0] == "en camino":
                        messagebox.showerror(title="Error",
                                                message="No se puede cambiar la entrega porque el delivery ya salió con los pedidos")
                        return 0

        except db.Error:
            messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
            return 0
        except Exception:
            messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
            return 0
        else:
            #no hay complicaciones con el estado de los pedidos
            return 1
            
def cambiar_entrega_pedidos(entrega, id_cliente, cursor):

    if not verificar_pedidos(id_cliente, entrega, cursor):
        return 0

    time.sleep(1)

    #if verificar_cargo_envio(id_cliente):
    #    cursor.execute("UPDATE CLIENTE SET idCARGOENVIO=0 WHERE idCLIENTE='%d'" % id_cliente)
    #    messagebox.showinfo(title="Error", message="se quito el cargo de envio para el cliente")
        
    if cursor:
        try:

            cursor.execute("UPDATE PEDIDO SET TIPOENTREGA='%s' WHERE idCLIENTE='%d' AND ESTADO='en proceso'" % (entrega, id_cliente))
            
            if entrega == "en puerta":
                #Posiblemente si el pedido lo entrega el delivery se aplique un cargo al envio
                #sino se aplico, solo realizaremos una transaccion mas.

                cursor.execute("UPDATE CLIENTE SET idCARGOENVIO=0 WHERE idCLIENTE='%d'" % id_cliente)
                #debemos quitar el envio del label envio
        
        except db.Error:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        except Exception:
            messagebox.showerror(title="Error", message="%s" % traceback.format_exc())
            return 0
        else:
            cursor.connection.commit()
            messagebox.showinfo("Exito", "Entrega cambiada con Exito.")

        
    

