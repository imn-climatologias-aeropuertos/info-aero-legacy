from tkinter import messagebox as MessageBox

from app.utils import logger


def box(type: str, title: str, message: str):
    if type == "warning":
        logger.info(f"Launching warning window, message: {message}")
        MessageBox.showwarning(title, message)
    elif type == "error":
        logger.info(f"Launching error window, message: {message}")
        MessageBox.showerror(title, message)
    elif type == "okcancel":
        logger.info(f"Launching okcancel window, message: {message}")
        result = MessageBox.askokcancel(title, message)
        return result
    elif type == "showinfo":
        logger.info(f"Launching showinfo window, message: {message}")
        MessageBox.showinfo(title, message)
    else:
        msg = "invalid messagebox type."
        logger.error(msg.capitalize())
        raise ValueError(msg)
