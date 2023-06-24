import re
from collections import namedtuple
from tkinter import Entry, Frame, Label, Radiobutton, StringVar

from app.__colors__ import blue, light_blue, white
from app.utils import logger

User = namedtuple("User", "name lname1 lname2 email abbr value")

USERS = [
    User(
        "Mónica",
        "Jiménez",
        "Murillo",
        "mjimenez",
        "MJM",
        "0",
    ),
    User("Priscilla", "Castro", "Víquez", "pcastro", "PCV", "1"),
    User("Raquel", "Salazar", "Víquez", "rsalazar", "RSV", "2"),
    User("Karla", "Chaves", "Hidalgo", "kchaves", "KCH", "3"),
    User("Otro usuario", "", "", "", "", "4"),
]


class OtherUser(Frame):
    def __init__(
        self, master=None, width=250, height=100, font_type="Verdana", font_size=10
    ):
        super().__init__(master)
        self.width = width
        self.height = height
        self.font_type = font_type
        self.font_size = font_size
        self.config(bg=white, width=self.width, height=self.height)
        self.grid(row=1, column=2)

        # Create entries
        self._create()

    def _create(self):
        logger.info("Creating OtherUser widgets.")
        self.name_label = Label(
            self,
            text="Nombre",
            fg=blue,
            bg=white,
            font=(self.font_type, self.font_size),
            padx=5,
        )
        self.name_label.grid(row=0, column=0)
        self.email_label = Label(
            self,
            text="Email",
            fg=blue,
            bg=white,
            font=(self.font_type, self.font_size),
            padx=5,
        )
        self.email_label.grid(row=1, column=0)
        self.name_entry = Entry(
            self, bg=white, bd=3, width=13, fg=blue, justify="center"
        )
        self.name_entry.grid(row=0, column=1)
        self.email_entry = Entry(
            self, bg=white, bd=3, width=13, fg=blue, justify="center"
        )
        self.email_entry.grid(row=1, column=1)

    def get_values(self):
        logger.info("Getting OtherUser values, name and email.")
        return self.name_entry.get(), self.email_entry.get()


class SelectUser(Frame):
    def __init__(
        self,
        master=None,
        width=100,
        height=100,
        font_type="Verdana",
        big_font=16,
        small_font=14,
    ):
        super().__init__(master)
        self.width = width
        self.height = height
        self.font_type = font_type
        self.big_font = big_font
        self.small_font = small_font
        self._padx = 8
        self._pady = 6
        self.config(bg=white, width=self.width, height=self.height)
        self.pack()

        logger.info("Creating select user widgets.")
        # Radio buttons sentinel variable
        self.rbtn_value = StringVar(self, "4")

        # Section title
        self.title = Label(
            self,
            text="SELECCIONE SU USUARIO",
            fg=blue,
            bg=white,
            font=(self.font_type, self.big_font),
            pady=self._pady + 10,
        )
        self.title.pack()

        self.data = Frame(self, bg=white)

        # Create radio buttons
        self._radio_buttons()
        # Create other user entries
        self.other_user = OtherUser(master=self.data, font_size=self.small_font)

        self.data.pack()

    def _radio_buttons(self):
        self._users = []
        row = 0
        column = 0
        pady = 0
        for user in USERS:
            if column > 2:
                column = 0
                row = 1
                pady = self._pady
            rbtn = Radiobutton(
                self.data,
                text=f"{user.name} {user.lname1}",
                variable=self.rbtn_value,
                value=user.value,
                bg=white,
                fg=light_blue,
                font=(self.font_type, self.small_font),
                highlightthickness=0,
                padx=self._padx,
                pady=pady,
            )
            rbtn.grid(row=row, column=column)
            column += 1

    def get_user(self):
        logger.info("Getting user data.")
        user_index = int(self.rbtn_value.get())
        if self.rbtn_value.get() in "0123":
            return USERS[user_index]

        # create other user and return
        name, email = self.other_user.get_values()
        if len(email) == 0:
            raise ValueError("Other user email must be not empty")

        list_name = name.split(" ")
        if len(list_name) == 1:
            raise ValueError("Please supply at least one last name")
        elif len(list_name) == 2:
            list_name.append("")

        other_user = list(list_name)
        other_user.append(email)
        other_user[-1] = re.sub(r"@.+", "", other_user[-1])
        other_abbr = "".join(el[0].upper() for el in list_name)
        return User(*other_user, other_abbr, "4")
