import glob
import os
import re
import tkinter as tk
from platform import system

import img2pdf
from PIL import ImageFont

from app.__colors__ import light_blue, white
from app.__version__ import version
from app.frames import Climatology, Ephemeris, Header, SelectUser, box, Footer
from app.utils import MONTHS, TODAY, VOLCANOES, date2str, extract, logger
from app.utils.create_view import (
    create_clima,
    create_map_img,
    create_taf,
    create_trend01,
    create_trend02,
    create_volcanic_ash,
    create_winds,
)


class App(tk.Tk):
    def __init__(self):
        logger.info("Initialize UI.")
        super().__init__()
        self.title(f"AeroInformes - {version}")
        self._set_window_size_and_position()
        self.geometry(
            f"{self.win_width}x{self.win_height}+{self.x_position}+{self.y_position}"
        )
        self.resizable(False, False)
        self.config(bg=white)

        # Set the app icon
        logger.info("Setting the app icon.")
        if system() == "Windows":
            self.iconbitmap("assets/icons/plane.ico")
        else:
            icon = tk.PhotoImage(file="assets/icons/plane.png")
            self.tk.call("wm", "iconphoto", self._w, icon)

        logger.info("Creating the frames of UI.")
        # Crete all frames
        logger.info("Creating the header frame.")
        self.header = Header(master=self, width=self.win_width, height=110)

        # self.extract_btn = tk.Button(
        #     self, text="Extraer", fg=white, bg=light_blue, command=self.extract_images
        # )
        # self.extract_btn.pack()

        logger.info("Creating the climatology frame.")
        self.clima = Climatology(
            master=self,
            width=self.win_width,
            big_font=self.big_font,
            small_font=self.small_font,
        )

        logger.info("Creating the select user frame.")
        self.select_user = SelectUser(
            master=self,
            width=self.win_width,
            big_font=self.big_font,
            small_font=self.small_font,
        )

        logger.info("Creating the ephemeris frame.")
        self.ephemeris = Ephemeris(master=self, big_font=self.big_font)

        # Footer buttons
        logger.info("Creating the bottom buttons.")
        Footer(master=self, create_command=self._create_report, exit_command=self.destroy)

        self._delete_images()

    def _delete_images(self):
        logger.info("Deleting the previous output images.")
        images = glob.glob("images/output/*")
        for img in images:
            os.remove(img)

        logger.info("Deleting the previous volcanic ash images.")
        for volcano in VOLCANOES:
            images = glob.glob(f"images/volcanoes/{volcano.dirname}/*")
            for img in images:
                os.remove(img)

    def _create_report(self):
        logger.info("Start creating report.")
        try:
            user = self.select_user.get_user()
        except IndexError as e:
            logger.error(f"Select user error. {e}.")
            box(
                "error",
                "Error al procesar usuario.",
                "Seleccionó otro usuario, pero no escribió su nombre y/o usuario de correo institucional.",
            )
            return

        try:
            map = self.header.sigwx_map
        except AttributeError as e:
            logger.error(f"SIGWX Map error. {e}.")
            result = box(
                "okcancel",
                "Error al abrir mapa SIGWX.",
                "No ha seleccionado el mapa de tiempo significante. ¿Desea continuar?",
            )
            if not result:
                logger.info("User select to stop process, exiting.")
                return
            logger.info("User select to continue process without SIGWX Map.")
            map = None

        try:
            docx = self.header.get_docx_files("tendencia")
        except AttributeError as e:
            logger.error(f"Trend .docx error. {e}.")
            result = box(
                "okcancel",
                "Error al abrir archivo .docx.",
                "No ha seleccionado el archivo de Tendencia de Aeropuertos. ¿Desea continuar?",
            )
            if not result:
                logger.info("User select to stop process, exiting.")
                return
            logger.info("User select to continue process without trend .docx.")
            docx = None

        data = {
            "title_font": ImageFont.truetype("assets/fonts/DejaVuSansMono.ttf", 86),
            "subtitle_font": ImageFont.truetype("assets/fonts/DejaVuSansMono.ttf", 68),
            "text_font": ImageFont.truetype("assets/fonts/DejaVuSansMono.ttf", 48),
            "table_font": ImageFont.truetype("assets/fonts/DejaVuSansMono.ttf", 40),
            "map": map,
            "docx": docx,
            "clima": self.clima.stations,
            "ephemeris": self.ephemeris.get_ephemeris_time(),
            "user": (user.name, user.email),
        }

        logger.info("Start creating the views.")
        # create map view
        logger.info("Creating the SIGWX Map view.")
        create_map_img("01_map.png", **data)

        # create aerodromes trend views
        logger.info("Creating the trend views.")
        create_trend01("02_trend.png", **data)
        create_trend02("03_trend.png", **data)

        # create volcanic ash forecast views
        logger.info("Creating the volcanic ash views.")
        extract(self.header.docx_files)
        img_num = 4
        for volcano in VOLCANOES:
            error = create_volcanic_ash(
                f"0{img_num}_vash.png", name=volcano.name, dir=volcano.dirname, **data
            )
            img_num += 1
            if error:
                return

        # create TAF view
        logger.info("Creating the TAF view.")
        error = create_taf("07_taf.png", **data)
        if error:
            return

        # create winds view
        logger.info("Creating the winds table view.")
        error = create_winds("08_winds.png", **data)
        if error:
            return

        # create climatology view
        logger.info("Creating the climatology and ephemeris view.")
        create_clima("09_clima.png", **data)

        # create pdf file
        self._create_pdf()

    def _create_pdf(self):
        logger.info("Creating the PDF document.")
        images = glob.glob("images/output/*")
        user = self.select_user.get_user()
        year = TODAY.year
        month = MONTHS[TODAY.month]

        # create path if not exists
        dirname = f"pdf/{year}/{month}"
        if not os.path.exists(dirname):
            logger.info(f"Path {dirname} doesn't exists, creating it.")
            os.makedirs(dirname)

        # create file path
        date = date2str(include_weekday=False)
        report_num = "N1" if TODAY.hour < 10 else "N2"
        file_name = f"{dirname}/Informe Aeronautico {report_num} {date} {user.abbr}.pdf"

        if os.path.exists(file_name):
            logger.info(
                f"Report {file_name} exists, asking to user if want to replace it."
            )
            result = box(
                "okcancel",
                f"AeroInformes - {version}",
                f"El {re.sub(r'(.*/)+', '', file_name)} ya existe. ¿Desea sobreescribirlo?",
            )
            if not result:
                logger.info(f"User choose do not replace {file_name}, exiting.")
                box(
                    "showinfo",
                    f"AeroInformes - {version}",
                    "El informe no ha sido creado.",
                )
                return
            logger.info(f"User choose to replace {file_name}.")

        logger.info(f"Writing images on {file_name}.")
        with open(file_name, "wb") as f:
            f.write(img2pdf.convert(sorted(images)))

        box("showinfo", f"AeroInformes - {version}", "Informe creado correctamente.")
        logger.info(f"Report created correctly, exiting.")

    def _set_font_size(self):
        logger.info(f"Setting UI font size.")
        self.big_font = round(self.win_width * 0.035)
        self.small_font = round(self.win_width * 0.022)

    def _set_window_size_and_position(self):
        logger.info(f"Setting UI window sizes.")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.win_width = round(screen_width * 0.40)
        self.win_height = round(screen_height * 0.70)
        if screen_height < 1000:
            self.win_height += 75
        self.x_position = screen_width // 2 - self.win_width // 2
        self.y_position = (
            screen_height // 2 - self.win_height // 2 - round(screen_height * 0.03)
        )

        # set the font sizes
        self._set_font_size()


if __name__ == "__main__":
    root = App()
    root.mainloop()
