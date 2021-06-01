"""construimos un calendarios para tkinter:
   eliminamos los saltos de linea y los espacios,
   guardamos el nombre del mes y los dias en un label.
   Los dias son guardados en campos Labels (pueden ser Buttons)
   para recuperar el dia al hacerle clic.
   El calendario se destruye por defecto"""

import calendar,time,datetime,os
from tkinter import *
from tkinter import messagebox



def calendario_tkinter(year,month,lenguaje):
    #El calendario por defecto es spanish
    calendario = calendar.month(year,month)
    posicion_anio=0
    posicion_dias=0
    dias_dobles=False
    dias=[]
    primer_dia,ultimo_dia = calendar.monthrange(year,month)
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

    for x in range(len(calendario)):
        if posicion_anio:
            if calendario[x] == "\n":
                posicion_dias=x
                break
        if calendario[x] == "\n":
            posicion_anio=x+1

    if lenguaje == 'spanish':
        label_year = meses[month-1]+ ' '+str(year)
    elif lenguaje == 'english':
        label_year = calendario[:posicion_anio-1]

    dias_calendario = calendario[posicion_dias+1:]
    month = calendario[posicion_anio:posicion_dias]

    for x in range(len(dias_calendario)):
        if ord(dias_calendario[x]) != 32 and ord(dias_calendario[x]) != 10:
            if ord(dias_calendario[x+1]) != 32 and ord(dias_calendario[x+1]) != 10:
                dias.append(dias_calendario[x:x+2])
                if ord(dias_calendario[x]) == 49:
                    dias_dobles=True
            if not dias_dobles:
                dias.append(dias_calendario[x])

    return dias,label_year,month,primer_dia,ultimo_dia

class Calendario:
    """El mes debe ser sin O adelante: 7/2018.
       Si destruir es True, el calendario 
       e destruye.al seleccionar un dia
       por defecto es True"""

    #si _retornar int es false fecha retornara 20/02/2019'
    #de lo contrario 20022019'

    def __init__(self, master, month, year, destruir=True, lenguaje='spanish',
                 retornar_int=False, devolver_foco=False, estado="normal"):
        self.master = master
        self._retornar_int = False
        if retornar_int:
            self._retornar_int = retornar_int

        #establecemos el ancho y alto, posicionamos al centro
        self.ancho= 250
        self.alto = 250
        self.posx = (self.master.winfo_screenwidth() - self.ancho) / 2
        self.posy = (self.master.winfo_screenheight() - self.alto) / 2
        
        #self.dimension = 250 #le doy una dimension aprox.
        
        self.destruir = destruir
        self.month = month
        self.year = year
        self.lenguaje = lenguaje
        self.fecha = None
        self.dia_mes = None
        self.label_mes = None
        self.devolver_foco = devolver_foco
        self.estado = estado
        
    def crear_calendario(self, fuente = None):
        ventana = Toplevel(self.master)
        ventana.protocol("WM_DELETE_WINDOW", lambda:self.destruir_calendario(ventana))
        ventana.title("Calendario")
        
        icono_ico = "calendar.ico"
        if fuente:
           self.fuente = fuente
        else:
            self.fuente = 'Tahoma'
        #Se usa bind en vez de ent.config(text=dia_actual,command=lambda dia_actual=dia_actual :self.seleccion_dia(dia_actual))
        #Bind obtiene el evento al precionar el boton, con lambda tenemos todo un proceso despues de precionarlo para acceder al dato.
            
        try:
            ventana.iconbitmap(os.path.join("iconos\\%s" % icono_ico))
        except Exception as e:
            pass
            
        ventana.focus_set()
        ventana.grab_set()
        ventana.resizable(0,0)
        
        #meses
        try:
            day, month, year, primer_dia, ultimo_dia = calendario_tkinter(self.year, self.month, self.lenguaje)#mes actual

        except TypeError:
            self.month = int(self.month)
            self.year  = int(self.year)
            day, month, year, primer_dia, ultimo_dia = calendario_tkinter(self.year, self.month, self.lenguaje)#mes actual
        except Exception as e:
            
            messagebox.showinfo(title="Error", message=u"No se pudo establecer el calendario en los días seleccionados\n"+
                                u"Se selecciona por defecto el primer mes del año %s"%e)
            self.year  = int(self.year)
            day, month, year, primer_dia, ultimo_dia = calendario_tkinter(self.year, 1, self.lenguaje)#mes actual
            
        try:
            proximo_mes = calendario_tkinter(self.year, self.month+1, self.lenguaje)
        except:
            #enero = 1
            proximo_mes = calendario_tkinter(self.year, 1, self.lenguaje)
        try:
            mes_anterior = calendario_tkinter(self.year, self.month-1, self.lenguaje)
        except:
            #diciembre = 12
            mes_anterior = calendario_tkinter(self.year, 12, self.lenguaje)

        #labels, frames
        frame_calendario = Frame(ventana)
        frame_labels = Frame(ventana)
        frame_year = Frame(ventana)
        self.label_mes = Label(frame_year,text=month,font=(self.fuente,10))
        frame_botones = Frame(ventana)
        
        posicion = 0
        insertar = False
        posicion2 = 0
        dia_mes_ant = len(mes_anterior[0]) - primer_dia
        month = ["Lu","Ma","Mi","Ju","Vi","Sa","Do"]
        dia_del_mes = datetime.datetime.now()
        dia_del_mes = dia_del_mes.day
        botones = []

        #botones
        boton_siguiente= Button(frame_botones,width=16,text="Mes Siguiente", state=self.estado,
                                command= lambda botones=botones, v=ventana: self.siguiente_anterior(botones, True, v))

        boton_anterior = Button(frame_botones,width=16,text="Mes Anterior", state=self.estado,
                                command= lambda botones=botones, v=ventana: self.siguiente_anterior(botones, False, v))

        #creamos el calendario
        dia_actual = 0

        for x in range(0,6):
            for y in range(0,7):
                ent = Label(frame_calendario,width=3)
                ent.bind("<Button-1>", lambda event, label=ent, v=ventana: self.seleccion_dia(event, label, v))
                ent.grid(row=x,column=y,padx=3,pady=2)

                if dia_mes_ant < len(mes_anterior[0]):
                    ent.config(text=mes_anterior[0][dia_mes_ant], state=DISABLED,font=(self.fuente,10))
                    dia_mes_ant+=1
                if posicion2:
                    dia = proximo_mes[0][posicion2-1]
                    ent.config(text=proximo_mes[0][posicion2-1], state=DISABLED,font=(self.fuente,10))
                if y >=primer_dia:
                    insertar = True
                if posicion < len(day) and insertar:
                    dia_actual = day[posicion]
                    posicion+=1
                    ent.config(text=dia_actual,font=(self.fuente,10))
                    if int(dia_actual) == dia_del_mes:
                        ent.config(relief=RAISED )
                        self.dia_mes = ent
                if posicion >= len(day):
                    posicion2+=1

                if x != 1:
                    label_dia = Label(frame_labels,text=month[y],font=(self.fuente,12),width=2)
                    label_dia.grid(row=1, column=y, padx=5,pady=2)
                botones.append(ent)
       
        boton_siguiente.grid(row=0,column=1)
        boton_anterior.grid(row=0,column=0)
        self.label_mes.grid(row=0,column=4)
        frame_year.grid()
        frame_labels.grid()
        frame_calendario.grid()
        frame_botones.grid()
        ventana.geometry("%dx%d+%d+%d" % (self.ancho, self.alto, self.posx, self.posy-50))
        
        while 1:
            if ventana.winfo_exists():
                ventana.update_idletasks()
                ventana.update()
            else:
                break
        

    def seleccion_dia(self, event, label, ventana):
        #Se agrega 0 al dia del mes
        #Si el mes es agosto = 8; se agrega 08
        #se comprueba que sean los dias de este mes != disabled
        #este proceso se realiza por una cuestion de gustos.

        x = event.widget.cget("state")
        dia = event.widget.cget("text")
        if not x == 'disabled':
            label.config(relief=SUNKEN)
            ventana.update_idletasks()
            ventana.update()
            if not self._retornar_int:
                if not len(dia) > 1:
                    dia = '0'+dia
                if self.month < 10:
                    self.month =  "0" + str(self.month)
                self.fecha = str(self.year) + "-" + str(self.month) + "-" + dia
            else:
                try:
                    dia = int(dia)
                except Exception as e:
                    print (u"%s, no se ha podido establecer el día seleccionado")
                    return 0
                self.fecha = dia, self.month, self.year
            time.sleep(0.1)

            if self.destruir:
                self.destruir_calendario(ventana)
            
        return 0

    def destruir_calendario(self, ventana):
        ventana.update_idletasks()
        ventana.update()

        if ventana.winfo_exists():
            ventana.destroy()

        self.comprobar_foco()
        
    def comprobar_foco(self):
        if self.devolver_foco:
            self.master.focus_set()
            self.master.grab_set()
            self.master.resizable(0,0)

    def siguiente_anterior(self, botones, opcion, ventana):
        #opcion 1 siguiente
        #opcion 2 anterior
        #opcion 3 actual
        ventana.update_idletasks()
        ventana.update()
        self.dia_mes.config(relief=FLAT)
        if opcion:
            if self.month < 12:
                self.month+=1
            else:
                self.month=1
                self.year+=1
        else:
            if self.month > 1:
                self.month-=1
            else:
                self.month=12
                self.year-=1
        day, month, year, primer_dia, ultimo_dia = calendario_tkinter(self.year,self.month,self.lenguaje)
        posicion = 0
        posicion2 = 1
        ultimos_dias = ultimo_dia - (primer_dia-1)
        self.label_mes.config(text=month)        
        
        for x in range(len(botones)):
            if x < primer_dia:
                botones[x].config(text=ultimos_dias,state=DISABLED)
                ultimos_dias+=1
            else:
                if posicion < len(day):
                    botones[x].config(text=day[posicion],state=ACTIVE)
                    posicion+=1
                else:
                    botones[x].config(text=posicion2,state=DISABLED)
                    posicion2+=1 
        return 
