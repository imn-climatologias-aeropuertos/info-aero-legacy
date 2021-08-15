from tkinter import Entry, Frame, Label

from dateutil import tz
from suntime import Sun

from app.__colors__ import blue, light_blue, white
from app.utils import TODAY, TOMORROW, logger


class Hour(Frame):
    def __init__(
        self,
        master=None,
        text="",
        width=40,
        height=10,
        row=0,
        column=0,
        font_type="Verdana",
        font_size=12,
        ephem="sunrise",
    ):
        super().__init__(master)
        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.font_type = font_type
        self.font_size = font_size
        self.ephem = ephem
        self.row = row
        self.column = column
        self._padx = 8
        self._pady = 6
        self.config(bg=white, width=self.width, height=self.height)
        self.grid(row=self.row, column=self.column)

        logger.info("Creating ephemeris entries.")
        # set time of ephemeris
        self._set_ephemeris()

        # set label
        self._label()

        # set entry
        self._entry()

    def _label(self):
        self.label = Label(
            self,
            text=self.text,
            fg=light_blue,
            bg=white,
            font=(self.font_type, self.font_size),
            padx=self._padx,
            pady=self._pady,
        )
        self.label.grid(row=0, column=0)

    def _entry(self):
        self.entry = Entry(self, bg=white, bd=3, width=8, fg=blue, justify="center")
        self.entry.grid(row=0, column=1)
        self.entry.insert(0, self.date.strftime("%I:%M %p"))

    def _set_ephemeris(self):
        logger.info(f"Setting ephemeris time: {self.ephem}.")
        sun = Sun(9.928069, -84.090725)
        tzone = tz.gettz("America/Costa_Rica")

        if self.ephem == "sunrise":
            d = sun.get_local_sunrise_time(date=TOMORROW, local_time_zone=tzone)
        else:
            d = sun.get_local_sunset_time(date=TODAY, local_time_zone=tzone)

        self.date = d


class Ephemeris(Frame):
    def __init__(
        self,
        master=None,
        width=100,
        height=100,
        font_type="Verdana",
        big_font=16,
        small_font=12,
    ):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.font_type = font_type
        self.big_font = big_font
        self.small_font = small_font
        self._padx = 8
        self._pady = 6
        self.config(bg=white, width=self.width, height=self.height)
        self.pack()

        # Section title
        self.title = Label(
            self,
            text="SALIDA Y PUESTA DEL SOL",
            fg=blue,
            bg=white,
            font=(self.font_type, self.big_font),
            pady=self._pady,
        )
        self.title.pack()

        self.data = Frame(self)

        # Set sunrise hour frame
        self.sunrise = Hour(master=self.data, text="Salida del Sol")
        self.sunset = Hour(
            master=self.data, text="Puesta del Sol", column=1, ephem="sunset"
        )

        self.data.pack()

    def get_ephemeris_time(self):
        logger.info(f"Getting ephemeris times.")
        return self.sunrise.entry.get(), self.sunset.entry.get()
