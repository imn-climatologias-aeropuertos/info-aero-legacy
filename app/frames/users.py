from collections import namedtuple
from tkinter import Entry, Frame, Label, Radiobutton, StringVar

from ..__colors__ import blue, light_blue, white

User = namedtuple("User", "name email value")

USERS = [
    User(
        "Mónica Jiménez",
        "mjimenez",
        "0",
    ),
    User("Karla Chaves", "kchaves", "1"),
    User("Raquel Salazar", "rsalazar", "2"),
    User("Felipe González", "fgonzalez", "3"),
    User("Otro usuario", "", "4"),
]


class OtherUser(Frame):
    def __init__(self, master=None, width=250, height=100, font_type="Verdana"):
        super().__init__(master)
        self.width = width
        self.height = height
        self.font_type = font_type
        self.config(bg=white, width=self.width, height=self.height)
        self.grid(row=1, column=2)

        # Create entries
        self._create()

    def _create(self):
        self.name_label = Label(
            self, text="Nombre", fg=blue, bg=white, font=(self.font_type, 14), padx=5
        )
        self.name_label.grid(row=0, column=0)
        self.email_label = Label(
            self, text="Email", fg=blue, bg=white, font=(self.font_type, 14), padx=5
        )
        self.email_label.grid(row=1, column=0)
        self.name_entry = Entry(
            self, bg=white, bd=3, width=13, fg=blue, relief="flat", justify="center"
        )
        self.name_entry.grid(row=0, column=1)
        self.email_entry = Entry(
            self, bg=white, bd=3, width=13, fg=blue, relief="flat", justify="center"
        )
        self.email_entry.grid(row=1, column=1)

    def get_values(self):
        return self.name_entry.get(), self.email_entry.get()


class SelectUser(Frame):
    def __init__(self, master=None, width=100, height=100, font_type="Verdana"):
        super().__init__(master)
        self.width = width
        self.height = height
        self.font_type = font_type
        self._padx = 8
        self._pady = 6
        self.config(bg=white, width=self.width, height=self.height)
        self.pack()

        # Radio buttons sentinel variable
        self.rbtn_value = StringVar(self, "4")
        print(self.rbtn_value.get())

        # Section title
        self.title = Label(
            self,
            text="SELECCIONE SU USUARIO",
            fg=blue,
            bg=white,
            font=(self.font_type, 18),
            pady=self._pady + 10,
        )
        self.title.pack()

        self.data = Frame(self, bg=white)

        # Create radio buttons
        self._radio_buttons()
        # Create other user entries
        self.other_user = OtherUser(master=self.data)

        self.data.pack()

    def _radio_buttons(self):
        self._users = []
        row = 0
        column = 0
        for user in USERS:
            if column > 2:
                column = 0
                row = 1
            rbtn = Radiobutton(
                self.data,
                text=user.name,
                variable=self.rbtn_value,
                value=user.value,
                bg=white,
                fg=light_blue,
                font=(self.font_type, 14),
                highlightthickness=0,
                padx=self._padx,
                pady=self._pady,
            )
            rbtn.grid(row=row, column=column)
            column += 1
    
    def get_user(self):
        user_index = int(self.rbtn_value.get())
        if self.rbtn_value.get() in "0123":
            return USERS[user_index]
        
        return User(*self.other_user.get_values(), "4")
