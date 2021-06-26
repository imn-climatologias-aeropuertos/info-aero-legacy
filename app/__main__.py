import tkinter as tk
from platform import system

from .__colors__ import light_blue, white
from .__version__ import version
from .frames import Climatology, Header, SelectUser
from .utils import extract


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"AeroInformes - {version}")
        self.set_window_size_and_position()
        self.geometry(
            f"{self.win_width}x{self.win_height}+{self.x_position}+{self.y_position}"
        )
        self.resizable(False, False)
        self.config(bg=white)

        # Set the app icon
        if system() == "Windows":
            self.iconbitmap("./app/assets/icons/plane.ico")
        else:
            icon = tk.PhotoImage(file="./app/assets/icons/plane.png")
            self.tk.call("wm", "iconphoto", self._w, icon)

        # Crete all frames
        self.header = Header(master=self, width=self.win_width, height=110)

        # self.extract_btn = tk.Button(
        #     self, text="Extraer", fg=white, bg=light_blue, command=self.extract_images
        # )
        # self.extract_btn.pack()

        self.clima = Climatology(master=self, width=self.win_width, big_font=self.big_font, small_font=self.small_font)

        self.select_user = SelectUser(master=self, width=self.win_width, big_font=self.big_font, small_font=self.small_font)
    
        tk.Button(text="Get values", command=self.print_user).pack()
    
    def print_user(self):
        print(self.select_user.get_user())

    def extract_images(self):
        for docx in self.header.docx_files:
            extract(docx)
    
    def set_font_size(self):
        self.big_font = round(self.win_width * 0.035)
        self.small_font = round(self.win_width * 0.022)
        print(self.big_font, self.small_font)

    def set_window_size_and_position(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.win_width = round(screen_width * 0.40)
        self.win_height = round(screen_height * 0.84)
        print(self.win_width, self.win_height)
        self.x_position = screen_width // 2 - self.win_width // 2
        self.y_position = (
            screen_height // 2 - self.win_height // 2 - round(screen_height * 0.03)
        )
        
        # set the font sizes
        self.set_font_size()


if __name__ == "__main__":
    root = App()
    root.mainloop()
