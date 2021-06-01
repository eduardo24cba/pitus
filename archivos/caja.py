from tkinter import ttk
from tkinter import messagebox

import tkinter as tk
import traceback, time

from archivos.funciones import crear_progressbar, marcar_activo, destruir_hijos, conectar_db

#si entramos a caja, debemos borrar los widgets creados con anterioridad


#c.execute(" select a.fecha, c.tipocuenta, c.debe, c.haber, m.tipomovimiento
# from movimientocontable m inner join asientocontable a on a.idASIENTO == m.idASIENTO inner join 
# cuenta c on c.idCUENTA == m.idCUENTA where a.fecha='2021-05-17'" )

def caja(parent, frame_tareas, ancho_frame_accesos, notebook, boton, botones):
    #acomodamos todos los widgets al ancho y alto de la resolucion de pantalla actual
    ancho = parent.winfo_width() - ancho_frame_accesos
    alto  = parent.winfo_height()

    if frame_tareas:
        destruir_hijos(frame_tareas)

    parent.after(100, crear_progressbar(frame_tareas, alto, ancho, "red"))

    if boton:
        marcar_activo(boton, botones)

    frame_tareas.configure(width=ancho, height=alto)

    tk.Label(frame_tareas, text="Welcome to caja").grid()
