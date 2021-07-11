from tkinter import messagebox as MessageBox
from app.utils import logger


def box(type: str, title: str, message: str):
    if type == "warning":
        logger.info("Launching warning window.")
        MessageBox.showwarning(title, message)
    elif type == "error":
        logger.info("Launching error window.")
        MessageBox.showerror(title, message)
    elif type == "okcancel":
        logger.info("Launching okcancel window.")
        result = MessageBox.askokcancel(title, message)
        return result
    elif type == "showinfo":
        logger.info("Launching showinfo window.")
        MessageBox.showinfo(title, message)
    else:
        msg = "invalid messagebox type."
        logger.error(msg.capitalize())
        raise ValueError(msg)
