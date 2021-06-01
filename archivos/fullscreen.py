import tkinter as tk

class Fullscreen(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self.__geom='600x600+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad,
            master.winfo_screenheight() - pad))
        
        #master.bind('<Escape>', self.nose)

    def nose(self, event):
        geom = self.master.winfo_geometry()
        self.master.geometry(self.__geom)
        self.__geom = geom

