import tkinter as tk
from platform import system

from PIL import Image, ImageDraw, ImageFont

from .__colors__ import light_blue, white
from .__version__ import version
from .frames import Climatology, Ephemeris, Header, SelectUser
from .utils import extract
from .utils.create_view import create_map_img, create_map_img2


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

    def _extract_images(self):
        for docx in self.header.docx_files:
            extract(docx)

    def _create_report(self):
        title_font = ImageFont.truetype("assets/fonts/verdana.ttf", 90)
        subtitle_font = ImageFont.truetype("assets/fonts/verdana.ttf", 75)
        text_font = ImageFont.truetype("assets/fonts/verdana.ttf", 55)
        print("Hora efemérides", self.ephemeris.get_ephemeris_time())
        create_map_img("01_map.png", title_font=title_font, subtitle_font=subtitle_font, map=self.header.sigwx_map)
        create_map_img2("02_map.png", font=text_font)

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
