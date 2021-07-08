from tkinter import messagebox as MessageBox

def box(type: str, title: str, message: str):
    if type == "warning":
        MessageBox.showwarning(title, message)
    elif type == "error":
        MessageBox.showerror(title, message)
    elif type == "okcancel":
        result = MessageBox.askokcancel(title, message)
        return result
    elif type == "showinfo":
        MessageBox.showinfo(title, message)
    else:
        raise ValueError("invalid messagebox type.")