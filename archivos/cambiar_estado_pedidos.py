from archivos.funciones import conectar_db, destruir_hijos
from archivos.generador_pedidos import verificar_estado
from archivos.contabilidad_negocio import crear_asiento_contable

from tkinter import messagebox

import traceback

def cambiar_estado(id_pedido, opcion, widgets, canvas, parent, scroll, tipo_entrega, lista_total_pedidos,
                   id_cliente=None, lista_frames=None, frame_canvas=None, dic_variables=None, tipo_producto=None,
                   cantidad_producto=None, dic_labels=None, frame_total_pedidos=None, frame_notebook=None,
                   menu=None, precio_menu=None):
    
    """
    Cambiamos el estado de los pedidos a despachado, delivery, anulado.
    y actualizamos los widgets y cantidades de la tabla dinamica.
    el id_cliente no es necesario en la opcion preparado
    lista_frames contiene todos los frames que se crean en el frame canvas
    los necesitamos para calcular el alto y determinar si lleva scroll o no
    lista_total_pedidos contiene el canvas total pedidos y el scroll total pedidos
    dic_labels contiene una lista cuyo primer elemento es nombre del producto y segundo cantidad
    """
    
    cursor, database = conectar_db()
        
    if cursor and database:
        try:
            if opcion == "preparado":
                cursor.execute("UPDATE PEDIDO SET ESTADO='%s' WHERE idPEDIDO=%d" % (opcion, id_pedido))

            elif opcion == "anular":
                consulta = messagebox.askyesno(title="Anular pedido", message=u"¿Desea realmente anular el pedido?")
                #debemos asegurarnos, tal vez presiono por error.
                if consulta:
                    cursor.execute("DELETE FROM PEDIDO WHERE idPEDIDO='%d'" % id_pedido)

                else:
                    return 0

            else:
                #consultamos que todos los pedidos esten preparados
                #sea la opcion que sea
                if not verificar_estado(id_cliente, opcion, tipo_entrega):
                    return 0
                else:
                    if opcion == "despachar":
                        cursor.execute("UPDATE PEDIDO SET ESTADO='%s' WHERE idPEDIDO=%d" % ("Despachado", id_pedido))
                        result = crear_asiento_contable(menu, "venta mercaderia", precio_menu, cursor)
                        if not result:
                            messagebox.showerror(title="Error", message="no se ha podido guardar la venta")
                            return 0
                        
                    else:
                        #delivery
                        cursor.execute("UPDATE PEDIDO SET ESTADO='%s' WHERE idPEDIDO=%d" % ("en camino", id_pedido))
                        #pasa a la bandeja delivery a la espera que regrese el delivery e indique que fueron entregados
                        #una vez que suceda eso, se sumara el dinero a la caja
                        
        
        except database.Error:
            messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s funcion cambiar_estado" % traceback.format_exc())
            return 0
        except Exception:
            messagebox.showerror(title="Error", message="No se pueden mostrar los pedidos.\n%s funcion cambiar_estado" % traceback.format_exc())
            return 0
        else:
            #borramos los widgets si salio todo ok
            #crearemos un relojito de 1 segundo que nos da tiempo de una transicion.
            for widget in widgets:
                widget.destroy()

                parent.update()

                canvas.update()
            
            frame_canvas.update()

            #si la longitud es de 3, significa que solo quedaron se eliminaron todos los pedidos
            #y solo quedan los labels cliente, menu y cantidad
            #procedemos a eliminar el frame
            if len(frame_canvas.winfo_children()) == 3:
                frame_canvas.destroy()
            
            parent.update()
            
            canvas.update()

            canvas.config(scrollregion=canvas.bbox("all"))

            alto_frames = 0
            
            #chekeamos los frames que se han creado en el create_windows
            #y extraemos el alto para saber si debe existir el scroll
            #primero debemos comprobar que el frame no se elimino en las lineas anteriores.
            contador = 0
            
            for frame in range(len(lista_frames[:])):
                
                if lista_frames[contador].winfo_exists():
                    
                    alto_frames += lista_frames[contador].winfo_height()
                    
                    contador += 1
                else:
                    #si no existe lo eliminamos de la lista
                    del lista_frames[contador]

            #si la lista de frames es 0, significa que no existen pedidos en el frame canvas
            #eliminamos el canvas

            if not len(lista_frames):
                #canvas.destroy()
                #scroll.destroy()
                #if lista_total_pedidos:
                #    lista_total_pedidos[0].destroy()
                #    lista_total_pedidos[1].destroy()
                destruir_hijos(frame_notebook)

                parent.after(1000, lambda: messagebox.showinfo("Aviso", "No existen pedidos por preparar"))
            else:
                if alto_frames < canvas.winfo_height():
                    scroll.grid_forget()
                if frame_total_pedidos:
                    #si eliminamos un pedido o le cambiamos el estado
                    #debemos actualizar la lista del total de pedidos por preparar
        
                    #actualizamos los labels que aparecen en el frame total pedidos
                    #obtenemos la variable
                    variable = dic_variables.get(tipo_producto)
                    
                    #restamos la cantidad que tenia el pedido
                    cantidad = variable.get() - cantidad_producto

                    #asignamos
                    variable.set(cantidad)

                    #mostramos los labels actualizados
                    label_nombre_producto, label_cantidad_producto = dic_labels.get(tipo_producto)

                    label_nombre_producto.config(text=tipo_producto)
                        
                    label_cantidad_producto.config(text="%d" % variable.get())

            cursor.connection.commit()

        finally:
            database.close()
    else:
        pass
            
