from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
from ..__colors__ import white, light_blue

class Header(Frame):
    
    
    def __init__(self, master=None, width=100, height=100):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.pack()
        self.config(bg=white, width=self.width, height=self.height)
        self.create_widgets()
    
    
    def create_widgets(self):
        # set the imn logo
        self.imn = ImageTk.PhotoImage(Image.open('./app/assets/img/logo_imn.png').resize(self._image_size(3.6), Image.ANTIALIAS))
        self.logo_imn = Label(self, image=self.imn, bd=0)
        self.logo_imn.grid(row=0, column=0, pady=10)
        
        self.space = Label(self, width=4, bg=white)
        self.space.grid(row=0, column=1)
        
        # set the button to add .docx files
        self.docx_button = Button(self, text="Agregar Mapa", fg=white, bg=light_blue, width=10, relief="flat")
        self.docx_button.grid(row=0, column=2)
        
        self.space = Label(self, width=4, bg=white)
        self.space.grid(row=0, column=3)
    
        # set the minae logo
        self.minae = ImageTk.PhotoImage(Image.open('./app/assets/img/logo_minae.png').resize(self._image_size(3, height_cut=30), Image.ANTIALIAS))
        self.logo_minae = Label(self, image=self.minae, bd=0, bg=white)
        self.logo_minae.grid(row=0, column=4, pady=10)
    
    
    def _image_size(self, factor, height_cut=0):
        width = self.width // factor
        height = self.width // factor * 2/3 - height_cut
        
        return round(width), round(height)
