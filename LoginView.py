from tkinter import *
from TkUtils import TkUtils as ut
from ErrorView import ErrorView
from model.application.League import league
from ManagerDashboardView import ManagerDashboardView
from model.exception.UnauthorisedAccessException import UnauthorisedAccessException

class LoginView:

    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.manager_id_entry = None
        self.login_btn = None

    def control(self):
        ut.image(self.root, "image/banner.png").pack()
        self.separator()
        login_lbl = ut.label(self.root, "Login")
        login_lbl.config(bg="#d9d9d9")
        login_lbl.pack(pady=(0, 10))
        self.separator()

        id_frame = Frame(self.root, bg="#d9d9d9")
        self.manager_id_lbl = ut.label(id_frame, "Manager ID:  ")
        self.manager_id_lbl.config(bg="#d9d9d9")
        self.manager_id_lbl.pack(side=LEFT)
        self.manager_id_entry = Entry(id_frame, width=30)
        self.manager_id_entry.pack(ipady=3)
        self.manager_id_entry.bind("<KeyRelease>", self.text_entered)
        id_frame.pack()

        btn_frame = Frame(self.root)
        self.login_btn = ut.button(btn_frame, "Login", self.try_login)
        self.login_btn.config(state=DISABLED)
        self.login_btn.pack(side=LEFT, expand=True, fill=X)
        root.bind("<Return>", self.enter_clicked)
        ut.button(btn_frame, "Exit", self.close).pack(side=LEFT, expand=True, fill=X)
        btn_frame.pack(expand=True, fill=X, pady=(10, 0))

    def text_entered(self, event):
        # If text is entered in the entry box, we set the state=NORMAL, otherwise state=DISABLED
        if self.manager_id_entry.get().strip():
            self.login_btn.config(state=NORMAL)
        else:
            self.login_btn.config(state=DISABLED)

    def separator(self):
        return ut.separator(self.root).pack(fill=X, pady=(0, 10))

    def try_login(self):
        manager_id_string = self.manager_id_entry.get()

        if not manager_id_string:
            return

        try:
            manager_id = int(manager_id_string)

            manager = self.model.validate_manager(manager_id)
            self.model.set_logged_in_manager(manager)
            self.close()
            ManagerDashboardView(self.model).show()

        except ValueError:
            ErrorView("Incorrect format for manager ID").show()
        except UnauthorisedAccessException as e:
            ErrorView(str(e)).show()
        except Exception as e:
            ErrorView("Unexpected error: " + str(e)).show()

    def close(self):
        self.root.destroy()

    def enter_clicked(self, event):
        self.try_login()


if __name__ == "__main__":
    root = ut.root()
    login = LoginView(root, league)
    login.control()
    root.mainloop()
