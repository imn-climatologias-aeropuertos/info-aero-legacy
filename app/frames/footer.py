from tkinter import Button, Frame, Label

from app.utils import Colors


class FooterButton(Button):
    def __init__(self, master=None, text="", command=None, column=0):
        super().__init__(
            master,
            text=text,
            padx=20,
            pady=10,
            fg=Colors.white,
            bg=Colors.light_blue,
            relief="flat",
            command=command,
        )

        self.grid(row=1, column=column, padx=20)


class Footer(Frame):
    def __init__(
        self, master=None, width=100, height=40, create_command=None, exit_command=None
    ):
        super().__init__(master, bg=Colors.white)

        # make space between previous frame and footer
        label = Label(self, width=10, height=0 - 5, bg=Colors.white)
        label.grid(row=0, column=0)

        # create button
        FooterButton(master=self, text="Crear Informe", command=create_command)

        # exit button
        FooterButton(master=self, text="Salir", command=exit_command, column=1)

        self.pack()
