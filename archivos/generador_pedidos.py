from archivos.funciones import conectar_db
from archivos.constantes import MSJ_DESPACHADOS, MSJ_DELIVERY
from tkinter import messagebox
import  traceback

def lista_de_pedidos(lista_ids, estado, cursor):
    """
    Devuelve un generador que realiza consulta a la base de datos
    extrayendo los distintos pedidos de los clientes
    """    
            
    for id_cliente in lista_ids:
            
        yield consulta_pedidos(id_cliente[0], estado, cursor)
        
        
def lista_ids_cliente(estado, cursor):
    """
    Consultamos si existen pedidos de clientes en el estado solicitado
    """
    print(estado)
    if cursor:
        lista_ids = cursor.execute("""SELECT c.idCLIENTE FROM PEDIDO pe
                                  INNER JOIN CLIENTE c ON c.idCLIENTE = pe.idCLIENTE
                                  WHERE ESTADO='%s' GROUP BY c.idCLIENTE""" % estado)
        lista_ids = lista_ids.fetchall()

        print(lista_ids)

        if not lista_ids:
            return []

        else:
            return lista_ids

def consulta_pedidos(id_cliente, estado, cursor):
    #retorna una lista de pedidos de un mismo cliente
    consulta = cursor.execute("""SELECT p.PRODUCTO, pe.CANTIDADPRODUCTO, c.NUMERACIONOLOTE, 
                                 c.CALLEOMANZANA, pe.ESTADO, pe.TIPOENTREGA,
                                 pe.FECHA, pe.HORACREACION, pe.idPEDIDO, pe.idCLIENTE, p.PRECIO FROM PEDIDO pe
                                 INNER JOIN PRODUCTO p ON p.idPRODUCTO = pe.idPRODUCTO
                                 INNER JOIN CLIENTE c ON c.idCLIENTE = pe.idCLIENTE
                                 WHERE ESTADO='%s' AND pe.idCLIENTE='%d' ORDER BY pe.HORACREACION AND pe.FECHA""" % (estado, id_cliente))
            
    consulta = consulta.fetchall()

    return consulta

def verificar_estado(id_cliente, opcion, tipo_entrega):
    cursor, database = conectar_db()

    if cursor:
        try:
            consulta = cursor.execute("""SELECT pe.ESTADO FROM PEDIDO pe
                                        INNER JOIN CLIENTE c ON pe.idCLIENTE = c.idCLIENTE
                                        WHERE c.idCLIENTE='%d'""" % id_cliente)
            consulta = consulta.fetchall()

            
            #si despachamos desde delivery no pueden existir pedidos que no esten en la bandeja delivery
            #si es en puerta tienen que estar preparados si o si
            #si la opcion es delivery, significa que pasan a la pestaña delivery, para que eso ocurra, 
            #ningun pedido debe estar en proceso

            for estado in consulta:
                if opcion == "despachar":
                    if tipo_entrega == "delivery":
                        if estado[0] in ("en proceso", "preparado"):
                            messagebox.showerror(messagebox.ERROR,
                                                 message=MSJ_DELIVERY)
                            return 0
                
                else:
                    #en puerta o delivery
                    if estado[0] in ("en proceso", ):
                        messagebox.showerror(messagebox.ERROR,
                                             message=MSJ_DELIVERY if opcion == "delivery" else MSJ_DESPACHADOS)
                        return 0
                        
                        
        except database.Error:
            messagebox.showerror(messagebox.ERROR, message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
            return 0
        except Exception:
            messagebox.showerror(messagebox.ERROR, message="No se pueden mostrar los pedidos.\n%s" % traceback.format_exc())
            return 0
        else:
            return 1

        finally:
            database.close()
