import re
from tkinter import Button, Frame, Label
from tkinter import filedialog as fd

from PIL import Image, ImageTk

from app.__colors__ import light_blue, white
from app.utils import logger


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
        logger.info(f"Creating header widgets.")
        # set the imn logo
        self.imn = ImageTk.PhotoImage(
            Image.open("assets/img/logo_imn.png").resize(
                self._image_size(3.6), Image.ANTIALIAS
            )
        )
        self.logo_imn = Label(self, image=self.imn, bd=0)
        self.logo_imn.grid(row=0, column=0, pady=10)

        # set space between images and buttons
        self.space = Label(self, width=4, bg=white)
        self.space.grid(row=0, column=1)

        # set the buttons to add SIGWX map and .docx files
        self.buttons = self._create_buttons()
        self.buttons.grid(row=0, column=2)

        # set space between images and buttons
        self.space = Label(self, width=4, bg=white)
        self.space.grid(row=0, column=3)

        # set the minae logo
        self.minae = ImageTk.PhotoImage(
            Image.open("assets/img/logo_minae.png").resize(
                self._image_size(3, height_cut=30), Image.ANTIALIAS
            )
        )
        self.logo_minae = Label(self, image=self.minae, bd=0, bg=white)
        self.logo_minae.grid(row=0, column=4, pady=10)

    def get_docx_files(self, dtype="avisos"):
        l = sorted(self.docx_files)
        if dtype == "tendencia":
            for i in range(len(l)):
                result = re.search(r"[Tt]enden[cs]ia", l[i])

                if result:
                    return l[i]

            logger.error("Trend file not found, raising AttributeError.")
            raise AttributeError("trend file not found.")
        return l[:3]

    def _select_map(self):
        filetypes = (
            ("JPG images", ".jpg"),
            ("JPEG images", ".jpeg"),
            ("PNG images", ".png"),
            ("GIF images", ".gif"),
            ("All files", "."),
        )

        logger.info("Open file dialog for asking SIGWX map path.")
        self.sigwx_map = fd.askopenfile(
            initialdir="/Images",
            title="Seleccione el Mapa SIGWX.",
            filetypes=filetypes,
        )
        # print(self.sigwx_map)

    def _select_docx_files(self):
        filetypes = (
            ("MS Word files", ".docx"),
            ("MS Word 97-2003 files", ".doc"),
            ("All files", "."),
        )

        logger.info("Open file dialog for asking .docx files path.")
        self.docx_files = fd.askopenfilenames(
            initialdir="/Documents",
            title="Seleccione los archivos de MS Word.",
            filetypes=filetypes,
        )

    def _create_buttons(self):
        logger.info("Creating header buttons.")
        __frame = Frame(self, bg=white)

        # set button: add map
        map_btn = Button(
            __frame,
            text="Agregar Mapa",
            fg=white,
            bg=light_blue,
            width=10,
            relief="flat",
            command=self._select_map,
        )
        map_btn.grid(row=0, column=0)

        # set space between buttons
        space = Label(__frame, width=2, bg=white)
        space.grid(row=1, column=0)

        # set button: add docx
        docx_btn = Button(
            __frame,
            text="Agregar .docx",
            fg=white,
            bg=light_blue,
            width=10,
            relief="flat",
            command=self._select_docx_files,
        )
        docx_btn.grid(row=2, column=0)

        return __frame

    def _image_size(self, factor, height_cut=0):
        width = self.width // factor
        height = self.width // factor * 2 / 3 - height_cut

        return round(width), round(height)
