from tkinter import *
from TkUtils import TkUtils as ut
from SwapView import SwapView
from TeamDashboardView import TeamDashboardView


class ManagerDashboardView:
    def __init__(self, league):
        self.league = league
        self.manager = league.get_logged_in_manager()
        self.team = self.manager.get_team()

    def show(self):
        self.window = ut.root()
        self.window.title("Manager Dashboard")

        ut.image(self.window, "image/banner.png").pack()
        self.separator()

        # Team name
        team_name = self.change_team_name()

        self.team_name_lbl = ut.label(self.window, team_name)
        self.team_name_lbl.config(font="Arial 12 bold", bg="#d9d9d9")
        self.team_name_lbl.pack(pady=(0, 10))
        ut.separator(self.window).pack(fill=X, pady=(0, 5))  # Didnt call separator() here as different pady values were to be used

        # The center frame needs to include two elements, first being the image of the jerse
        # And the second being the mid-buttons
        self.center_frame = Frame(self.window, bg="#d9d9d9")
        self.center_frame.pack(pady=(0, 5))


        # jersey img
        jersey_img = self.change_jersey_img()
        self.jersey = ut.image(self.center_frame, jersey_img, height=200, width=200, background="#d9d9d9")
        self.jersey.pack()


        # mid-button frame
        self.mid_btn_frame = Frame(self.center_frame, bg="#d9d9d9", width=250, height=30)
        # withdraw-btn
        self.withdraw_btn = ut.button(self.mid_btn_frame, "Withdraw", callback=self.withdraw_team)
        self.withdraw_btn.pack(side=LEFT, fill=X, expand=True, ipadx=25)
        # manage-btn
        self.manage_btn = ut.button(self.mid_btn_frame, "Manage", callback=self.open_team_dashboard)
        self.manage_btn.pack(side=LEFT, fill=X, expand=True, ipadx=25)
        # checking if buttons to be disabled
        self.disable_mid_btns()
        # packt the mid-btn frame
        self.mid_btn_frame.pack()


        # bottom-frame
        bottom_btn_frame = Frame(self.window)
        # swap-team btn
        ut.button(bottom_btn_frame, "Swap Team", callback=self.open_swap_view).pack(side=LEFT, fill=X, expand=True)
        # close-team btn
        ut.button(bottom_btn_frame, "Close", callback=self.close).pack(side=LEFT, fill=X, expand=True)
        # pack the btm-btn frame
        bottom_btn_frame.pack( fill=X, expand=True, pady=(5, 0))

        self.window.mainloop()

    def separator(self):
        return ut.separator(self.window).pack(fill=X, pady=(0, 10))

    def change_team_name(self):
        if self.team:
            return str(self.team)
        return "No team"

    def change_jersey_img(self):
        if self.team:
            return f"image/{self.team.get_team_name().lower()}.png"
        return "image/none.png"

    def withdraw_team(self):
        if self.manager.get_team():
            self.league.withdraw_manager_from_team(self.manager)
            self.update_team_display()

    def update_team_display(self):

        self.team = self.manager.get_team()

        team_name = self.change_team_name()
        jersey_img = self.change_jersey_img()
        self.disable_mid_btns()

        self.team_name_lbl.config(text=team_name)

        self.jersey.destroy()
        self.jersey = ut.image(self.center_frame, jersey_img, height=200, width=200, background="#d9d9d9")
        self.jersey.pack(before=self.mid_btn_frame)
        self.disable_mid_btns()

    def disable_mid_btns(self):
        if self.team:
            self.withdraw_btn.config(state=NORMAL)
            self.manage_btn.config(state=NORMAL)
        else:
            self.withdraw_btn.config(state=DISABLED)
            self.manage_btn.config(state=DISABLED)

    def open_team_dashboard(self):
        self.window.destroy()
        TeamDashboardView(self.league).show()

    def open_swap_view(self):
        manageable_teams = []
        for t in self.league.get_manageable_teams().get_teams():
            manageable_teams.append(str(t))
        SwapView(self, manageable_teams).show()

    def close(self):
        self.window.destroy()
