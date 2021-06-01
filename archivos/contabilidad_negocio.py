from archivos.funciones import conectar_db, obtener_fecha
from tkinter import messagebox

import traceback

def crear_asiento_contable(tipo_movimiento, operacion, monto, cursor):
    """
    tipo de movimento: puede ser compra, venta, etc.
    operacion: el tipo de compra, de venta, etc
    monto: la cantidad que se abono o ingreso
    """

    if obtener_fecha(fecha=True):
        fecha_creacion = obtener_fecha(fecha=True)
    else:
        messagebox.showerror(messagebox.ERROR, "No se ha podido obtener la fecha")
        return 0

    if cursor:
        try:
            cursor.execute("INSERT INTO ASIENTOCONTABLE(FECHA) VALUES('%s')" % fecha_creacion)
            id_asiento = cursor.lastrowid
            
            if operacion == "compra mercaderia":

                cursor.execute("INSERT INTO CUENTA(TIPOCUENTA, HABER) VALUES('caja', '%d')" % monto)
                id_cuenta_caja = cursor.lastrowid
                
                cursor.execute("INSERT INTO CUENTA(TIPOCUENTA, DEBE) VALUES('mercaderia', '%d')" % monto)
                id_cuenta_merc = cursor.lastrowid

                cursor.execute("""INSERT INTO MOVIMIENTOCONTABLE(idASIENTO, idCUENTA, DEBEOHABER, TIPOMOVIMIENTO) 
                               VALUES('%d', '%d', '%d', '%s')""" % (id_asiento, id_cuenta_caja, 1, tipo_movimiento))
                
                cursor.execute("""INSERT INTO MOVIMIENTOCONTABLE(idASIENTO, idCUENTA, DEBEOHABER, TIPOMOVIMIENTO) 
                               VALUES('%d', '%d', '%d', '%s')""" % (id_asiento, id_cuenta_merc, 0, tipo_movimiento))

            elif operacion == "venta mercaderia":
              
                cursor.execute("INSERT INTO CUENTA(TIPOCUENTA, DEBE) VALUES('caja', '%d')" % monto)
                id_cuenta_caja = cursor.lastrowid

                cursor.execute("INSERT INTO CUENTA(TIPOCUENTA, HABER) VALUES('ventas', '%d')" % monto)
                id_cuenta_venta = cursor.lastrowid

                print((id_asiento, id_cuenta_caja, 0, tipo_movimiento))

                #al ser una venta generamos un ingreso en caja -> debe
                cursor.execute("""INSERT INTO MOVIMIENTOCONTABLE(idASIENTO, idCUENTA, DEBEOHABER, TIPOMOVIMIENTO) 
                               VALUES('%d', '%d', '%d', '%s')""" % (id_asiento, id_cuenta_caja, 0, tipo_movimiento))

                #generamos una venta en la cuenta ventas
                cursor.execute("""INSERT INTO MOVIMIENTOCONTABLE(idASIENTO, idCUENTA, DEBEOHABER, TIPOMOVIMIENTO) 
                               VALUES('%d', '%d', '%d', '%s')""" % (id_asiento, id_cuenta_venta, 1, tipo_movimiento))

            cursor.connection.commit()


        except Exception:
            messagebox.showerror(messagebox.ERROR, "%s" % traceback.format_exc())
            return 0 
        except database.Error:
            messagebox.showerror(messagebox.ERROR, "%s" % traceback.format_exc())
            return 0

        else:
            #retornamos 1 para la funcion que nos llama
            return 1

    else:
        messagebox.showerror(messagebox.ERROR, "No se pudo conectar a la base de datos, funcion crear_asiento_contable")
        return 0
        
