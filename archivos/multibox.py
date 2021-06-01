import tkinter as tk
import traceback

class MultiListbox(tk.Frame):
    def __init__(self, master, lists, alto=None, font=None, function=None, args=None, factura=False,
                 expand_total=None, menu=False, alto_ancho=None, selectbackground=None, bg=None, alineacion="n"):
        tk.Frame.__init__(self, master)
        scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        #el alto es la cantidad de filas a mostrar
        #menu en listbox
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Modificar",command=lambda mensaje="Hello Wordl":showinfo(title="Mensaje",message=mensaje))
        self.alto  = 0
        self.ancho = 0
        self.alineacion = alineacion
        
        #ancho y alto de la ventana para mostrar la lista
        if expand_total:
            #el ultimo elemento de la lista no se muestra
            #se le da un borderwidth de x y al ancho se le resta el doble
            x = 6
            self.ancho = self.ancho - x*2
            #se crea un canvas, se configura el scroll
            canvas = tk.Canvas(self, xscrollcommand=scroll.set, width=self.ancho, height=self.alto, borderwidth=x)
            if bg:
                canvas.config(bg=bg)
            scroll.config(command=canvas.xview)
            #frame que contiene todas las listbox que creamos
            #el frame no se packea para que funcione
            frame_listbox = tk.Frame(canvas, width=self.ancho, height=self.alto )
            #creamos nuevos frames dentro de la ventana principal
            #estos se desplazan con el scroll
            canvas.create_window(0, 0, window=frame_listbox, anchor="nw")
        else:
            frame_listbox = self

        if alto_ancho:
            self.alto, self.ancho = alto_ancho

            self.config(width=self.ancho, height=self.alto)

            #esto le dice al frame que mantenga el tamaño dado por mas que los widgets hijos sean mas grandes
            #esto tambien hace que la listbox se expanda en todas las direcciones, justo lo que necesitamos ahora
            self.pack_propagate(0)

        #color de factura
        color_seleccion = "blue"
        if factura:
            color_seleccion = "black"

        #Patterns
        self.principal = master
        #funcion que se pasa como referencia
        #para luego llamarla desde aca
        self.__funcion = function
        self.__argumentos = args
        

        self.fuente = font if font else ('Tahoma',12,'bold')

        #lista que contiene las listbox
        self.lists = []
        
        frame_scroll = tk.Frame(self); frame_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(frame_scroll, borderwidth=1, relief=tk.RAISED).pack(fill=tk.X)
        sb = tk.Scrollbar(frame_scroll, orient=tk.VERTICAL, command=self._scroll)
        sb.pack(expand=tk.YES, fill=tk.Y)
        
        for l,w in lists:
            frame = tk.Frame(frame_listbox)

            frame.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

            tk.Label(frame, text=l, borderwidth=0, bg="#7e6e86",
                  fg='#f1f1f1', relief=tk.GROOVE, font=self.fuente,
                  anchor=self.alineacion).pack(fill=tk.X)
            
            #configuramos la listbox solo para el programa pedidos
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=tk.FLAT, exportselection=tk.FALSE, font=self.fuente,
                         selectforeground=color_seleccion, selectmode = "multiple")

            lb.pack(expand=True, fill=tk.BOTH)

            if alto:
                lb.configure(height=alto)

            self.lists.append(lb)

            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            lb.bind("<Double-Button-1>", lambda e, widget=lb :self.doble_clic(e,widget))

            if menu:#si necesitamos usar menu
                lb.bind("<Button-3>", self.menu_)
        
        self.update()

        if expand_total:
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.pack(expand=True, fill=tk.BOTH)
            scroll.pack(side=tk.BOTTOM, fill=tk.X)
        


        self.lists[0]['yscrollcommand']=sb.set
        
    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, tk.END)
        self.selection_set(row)
        return 'break'

    def _item_seleccionado(self, index, color):
        print("color")
        for item in range(len(self.lists)):
            self.lists[item].itemconfigure(index, bg=color)
        return

    def doble_clic(self,event,widget):
        #IndexError evita error cuando la listbox esta vacia
        seleccionado = widget.curselection()
        try:
            seleccionado = seleccionado[0]
        except IndexError:
            return 0
        widget = widget.get(seleccionado,seleccionado)
        widget = widget[0]
        if widget == 'No cargado':
            self.__funcion(self.__argumentos[0],self.__argumentos[1],self.__argumentos[2])
            self.principal.destroy()
        return

    def activate(self, index):
        #color de fondo igual
        color = None
        
        try:
            for item in range(len(self.lists)):
                color = self.lists[item].itemcget(index,'bg')
                self.lists[item].select_set(index)
                if color:
                    self.lists[item].config(selectbackground=color)
                else:self.lists[item].config(selectbackground='white')
        except Exception:
            messagebox.showinfo(title="Aviso", message="Sacar foto y enviarmela\n%s" % traceback.format_exc())
            pass

        return
        
    def menu_(self,event):
        try:
            self.menu.tk_popup(event.x_root+48,event.y_root+14,0)
        finally:
            self.menu.grab_release()
            
    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            if args[0] == 'scroll':
                l.yview_scroll(args[1],args[2])
            elif args[0] == 'moveto':
                l.yview_moveto(args[1])
                
    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        #if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        #color de fondo igual
        color = None
        try:
            for l in self.lists:
                color = l.itemcget(first,'bg')
                l.selection_set(first, last)
                if color:
                    l.config(selectbackground=color)
                else:l.config(selectbackground='white')
        except Exception:
            pass

