from tkinter import Button, Label, Frame, Entry
from ..__colors__ import white, light_blue, blue

class Station(Frame):
    
    def __init__(self, master=None, row=0, name="generic", width=100, height=10, font_type="Verdana", padx=8, pady=0):
        super().__init__(master)
        self.master = master
        self.name = name
        self.font_type = font_type
        self.width = width
        self.height = height
        self._row = row
        self._padx = padx
        self._pady= pady
        
        self._create_entries()
    
    def _create_entries(self):
        # labels and entries
        Label(self.master, text=self.name.upper(), fg=light_blue, bg=white, font=(self.font_type, 14), padx=self._padx, pady=self._pady).grid(row=self._row, column=0)
        self.tmax = self._entry(1)
        self.tmin = self._entry(2)
        self.prec = self._entry(3)
    
    def _entry(self, column):
        entry = Entry(self.master, bg=white, bd=3, width=5, fg=blue, relief="flat", justify="center")
        entry.grid(row=self._row, column=column)
        return entry
    
    def get_values(self):
        return self.tmax.get(), self.tmin.get(), self.prec.get()

class Climatology(Frame):
    
    def __init__(self, master=None, width=100, height=100, font_type="Verdana"):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.font_type = font_type
        self._pady = 6
        self._padx = 8
        self.pack()
        self.config(bg=white, width=self.width, height=self.height)
        
        # Section title
        self.title = Label(self, text="CLIMATOLOGÍA DE LOS AEROPUERTOS", fg=blue, bg=white, font=(self.font_type, 18), pady=self._pady)
        self.title.pack()
        
        # Create stations frame
        self.data = Frame(self, bg=white)
        
        # Variables names
        self.labels = []
        self._create_var_labels()
        
        # Station frames
        self.stations = [
            Station(master=self.data, row=1, name="mroc", width=self.width, font_type=self.font_type, padx=self._padx, pady=self._pady),
            Station(master=self.data, row=2, name="mrpv", width=self.width, font_type=self.font_type, padx=self._padx),
            Station(master=self.data, row=3, name="mrlb", width=self.width, font_type=self.font_type, padx=self._padx, pady=self._pady),
            Station(master=self.data, row=4, name="mrlm", width=self.width, font_type=self.font_type, padx=self._padx),
        ]
        
        self.data.pack()
        
        Button(text="Get values", command=self.climatology_values).pack()
    
    def climatology_values(self):
        for station in self.stations:
            print(station.get_values())
    
    def _label(self, text, row, column):
        lb = Label(self.data, text=text, fg=light_blue, bg=white, font=(self.font_type, 14), padx=self._padx)
        lb.grid(row=row, column=column)
        self.labels.append(lb)
    
    def _create_var_labels(self, row=0):        
        self._label("Estación", row, 0)
        self._label("T. Máxima", row, 1)
        self._label("T. Mínima", row, 2)
        self._label("Precipitación", row, 3)