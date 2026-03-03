from tkinter import *
from TkUtils import TkUtils as ut


class ErrorView:
    def __init__(self, message):
        self.message = message

    def show(self):
        window = ut.top_level("Error")

        ut.image(window, "image/error.png").pack()
        ut.separator(window).pack(fill=X, pady=(0, 10))

        exception_name_lbl = ut.label(window, "UnauthorisedAccessException")
        exception_name_lbl.config(font="Arial 14 bold", fg="red", bg="#d9d9d9")
        exception_name_lbl.pack(pady=(0, 5))
        ut.separator(window).pack(fill=X, pady=(10, 10))

        msg_lbl = ut.label(window, self.message)
        msg_lbl.config(bg="#d9d9d9")
        msg_lbl.pack(pady=(0, 10))

        btn_frame = Frame(window)
        ut.button(btn_frame, "Close", window.destroy).pack(side=LEFT, expand=True, fill=X)
        btn_frame.pack(expand=True, fill=X)

        window.mainloop()
