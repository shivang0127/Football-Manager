from tkinter import *
from TkUtils import TkUtils as ut


class SwapView:
    def __init__(self, dashboard, available_teams):
        self.dashboard = dashboard
        self.league = dashboard.league
        self.manager = dashboard.manager
        self.available_teams = available_teams
        self.selected_team = None
        self.window = None

    def show(self):
        self.window = ut.top_level("Swap")
        ut.image(self.window, "image/banner.png").pack()

        # Title section
        self.separator()
        lbl = ut.label(self.window, "Swap Team")
        lbl.config(font="Arial 12 bold", bg="#d9d9d9")
        lbl.pack(pady=(0, 10))
        self.separator()

        # Treeview for teams
        self.teams_tree = ut.treeview(self.window, ["Teams"], width=520)
        self.populate_tree()
        self.teams_tree.pack(pady=(0, 10))

        # Buttons frame
        bottom_btn_frame = Frame(self.window)
        self.swap_btn = ut.button(bottom_btn_frame, "Swap", callback=self.swap_team)
        self.swap_btn.config(state=DISABLED)
        self.swap_btn.pack(side=LEFT, expand=True, fill=X)

        ut.button(bottom_btn_frame, "Close", callback=self.close).pack(side=LEFT, expand=True, fill=X)
        bottom_btn_frame.pack(fill=X)

        # Selection binding
        self.teams_tree.bind("<<TreeviewSelect>>", self.treeview_select)

        self.window.mainloop()

    def separator(self):
        return ut.separator(self.window).pack(fill=X, pady=(0, 10))

    def populate_tree(self):
        # First we need to delete all the current teams in the treeview
        # As this method might be getting called after we swapped teams,
        # implying we would need to change the treeview
        # for which we first delete everything, then repopulate it with new manageable teams
        for team in self.teams_tree.get_children():
            self.teams_tree.delete(team)

        manageable_teams = self.league.get_manageable_teams().get_teams()
        for team in manageable_teams:
            self.teams_tree.insert("", END, values=[str(team)])

    def treeview_select(self, event):
        selected = self.teams_tree.selection()
        if selected:
            self.selected_team = self.teams_tree.item(selected[0])["values"][0]
            self.swap_btn.config(state=NORMAL)
        else:
            self.selected_team = None
            self.swap_btn.config(state=DISABLED)

    def swap_team(self):
        if not self.selected_team:
            return

        # Find selected team object from league
        target_team = None
        for team in self.league.get_manageable_teams().get_teams():
            if str(team) == self.selected_team:
                target_team = team
                break

        if not target_team:
            return

        # Perform model-level swap
        self.league.set_manager_for_team(self.manager, target_team)

        # Refresh dashboard and tree
        self.dashboard.update_team_display()
        self.populate_tree()

        # # Disable button again
        self.swap_btn.config(state=DISABLED)
        self.selected_team = None

    def close(self):
        self.window.destroy()
