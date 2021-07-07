import tkinter as tk
from platform import system

from PIL import Image, ImageDraw, ImageFont

from .__colors__ import light_blue, white
from .__version__ import version
from .frames import Climatology, Ephemeris, Header, SelectUser, box
from .utils import VOLCANOES, extract
from .utils.create_view import (create_clima, create_map_img, create_taf, create_trend01,
                                create_trend02, create_volcanic_ash,
                                create_winds)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"AeroInformes - {version}")
        self._set_window_size_and_position()
        self.geometry(
            f"{self.win_width}x{self.win_height}+{self.x_position}+{self.y_position}"
        )
        self.resizable(False, False)
        self.config(bg=white)

        # Set the app icon
        if system() == "Windows":
            self.iconbitmap("assets/icons/plane.ico")
        else:
            icon = tk.PhotoImage(file="assets/icons/plane.png")
            self.tk.call("wm", "iconphoto", self._w, icon)

        # Crete all frames
        self.header = Header(master=self, width=self.win_width, height=110)

        # self.extract_btn = tk.Button(
        #     self, text="Extraer", fg=white, bg=light_blue, command=self.extract_images
        # )
        # self.extract_btn.pack()

        self.clima = Climatology(
            master=self,
            width=self.win_width,
            big_font=self.big_font,
            small_font=self.small_font,
        )

        self.select_user = SelectUser(
            master=self,
            width=self.win_width,
            big_font=self.big_font,
            small_font=self.small_font,
        )

        self.ephemeris = Ephemeris(master=self, big_font=self.big_font)

        # Footer buttons
        tk.Label(self, width=self.win_width, height=0 - 5, bg=white).pack()
        tk.Button(
            self,
            text="Crear Informe",
            pady=10,
            padx=20,
            relief="flat",
            fg=white,
            bg=light_blue,
            command=self._create_report,
        ).pack()
        tk.Label(self, width=self.win_width, height=0 - 5, bg=white).pack()
        tk.Button(
            self,
            text="Salir",
            relief="flat",
            fg=white,
            bg=light_blue,
            command=self.destroy,
        ).pack()

    def _extract_images_from_docx(self):
        for docx in self.header.docx_files[:-1]:
            extract(docx)

    def _create_report(self):
        user = self.select_user.get_user()
        
        try:
            map = self.header.sigwx_map
        except AttributeError:
            box("error", "Error al abrir mapa SIGWX.", "No ha seleccionado el mapa de tiempo significante.")
        
        try:
            docx = self.header.get_docx_files("tendencia")
        except AttributeError:
            box("error", "Error al abrir archivo .docx.", "No ha seleccionado el archivo de Tendencia de Aeropuertos.")
            
        
        data = {
            "title_font": ImageFont.truetype("assets/fonts/JetBrainsMono-Regular.ttf", 86),
            "subtitle_font": ImageFont.truetype("assets/fonts/JetBrainsMono-Regular.ttf", 68),
            "text_font": ImageFont.truetype("assets/fonts/JetBrainsMono-Regular.ttf", 48),
            "table_font": ImageFont.truetype("assets/fonts/JetBrainsMono-Regular.ttf", 40),
            "map": map,
            "docx": docx,
            "clima": self.clima.stations,
            "ephemeris": self.ephemeris.get_ephemeris_time(),
            "user": (user.name, user.email),
        }
        
        # create map view
        create_map_img("01_map.png", **data)
        
        # create aerodromes trend views
        create_trend01("02_trend.png", **data)
        create_trend02("03_trend.png", **data)

        # create volcanic ash forecast views
        self._extract_images_from_docx()
        img_num = 4
        for volcano in VOLCANOES:
            create_volcanic_ash(
                f"0{img_num}_vash.png",
                name=volcano.name,
                dir=volcano.dirname,
                **data
            )
            img_num += 1
        
        # create TAF view
        create_taf("07_taf.png", **data)
        
        # create winds view
        create_winds("08_winds.png", **data)
        
        # create climatology view
        create_clima("09_clima.png", **data)
        
        box("showinfo", f"AeroInformes - {version}", "Carpeta creada correctamente.")

    def _set_font_size(self):
        self.big_font = round(self.win_width * 0.035)
        self.small_font = round(self.win_width * 0.022)

    def _set_window_size_and_position(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.win_width = round(screen_width * 0.40)
        self.win_height = round(screen_height * 0.84)
        self.x_position = screen_width // 2 - self.win_width // 2
        self.y_position = (
            screen_height // 2 - self.win_height // 2 - round(screen_height * 0.03)
        )

        # set the font sizes
        self._set_font_size()


if __name__ == "__main__":
    root = App()
    root.mainloop()
